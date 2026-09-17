from urllib.parse import urlparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import col as spark_col, lit
import os, yaml


def database_config(config_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.abspath(os.path.join(base_dir, config_path))

    with open(full_path, "r") as f:
        config = yaml.safe_load(f)
    project_root = os.path.dirname(os.path.dirname(full_path))

    csv_path = os.path.join(project_root, config["csv_path"])
    jar_path = os.path.join(project_root, config["postgres_jar_path"])

    print("Loaded config:", config)
    print("Loaded CSV path:", csv_path)

    return config, csv_path, jar_path


class Database_Creation:
    def __init__(self, spark: SparkSession, config: dict):
        self.spark = spark

        jdbc_url = config["database_url"]
        without_prefix = jdbc_url.replace("jdbc:postgresql://", "")
        hostport, dbname = without_prefix.split("/")
        host, port = hostport.split(":")

        self.host = host
        self.port = int(port)
        self.db_name = dbname
        self.user = config["db_user"]
        self.password = config["db_password"]
        self.db_url = jdbc_url


    def create_database_if_not_exists(self):
        print("Connecting to database ...")
        conn = psycopg2.connect(
            dbname="postgres",
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.db_name,))
        exists = cur.fetchone()

        if not exists:
            cur.execute(f'CREATE DATABASE "{self.db_name}"')
            print(f"Created database: {self.db_name}")
        else:
            print(f"Database {self.db_name} already exists")

        cur.close()
        conn.close()
        return not exists
    
    def spark_connection(self, df:DataFrame, table_name:str, mode:str):
        print(f"Loading Spark Dataframe/SQL into '{table_name}' and '{mode}' to the Table.")
        properties = {
            "user": self.user,
            "password": self.password,
            "driver": "org.postgresql.Driver"
        }
        
        if mode in ("append", "overwrite"):
            df.write \
                .format("jdbc") \
                .option("url", self.db_url) \
                .option("dbtable", table_name) \
                .options(**properties) \
                .mode(mode) \
                .save()
        elif mode == "read":
            result_df = self.spark.read \
                .format("jdbc") \
                .option("url", self.db_url) \
                .option("dbtable", table_name) \
                .option(**properties) \
                .load()
            print("Read complete.")
            return result_df
                
        else: 
            raise ValueError(f"{mode} feature is unavailable. \n Expected: append, overwrite, read")
                
        
    def load(self, df: DataFrame, table_name: str, mode="append"):
        print(f"Loading Spark DataFrame into '{table_name}'...")
        self.spark_connection(df, table_name, mode)
        print("Load complete.")

    def helper_column_creation(self, new_df: DataFrame, table_name: str):
        
        existing_df = self.spark_connection(None, table_name, mode="read")
        existing_cols = existing_df.columns
        
        new_cols = new_df.columns
        all_cols = list(set(existing_cols) | set(new_cols))

        for c in all_cols:
            if c not in existing_cols:
                existing_df = existing_df.withColumn(c, lit(None).cast(StringType()))
            else:
                existing_df = existing_df.withColumn(c, spark_col(c).cast(StringType()))
            if c not in new_cols:
                new_df = new_df.withColumn(c, lit(None).cast(StringType()))
            else:
                new_df = new_df.withColumn(c, spark_col(c).cast(StringType()))

        existing_df = existing_df.select(all_cols)
        new_df = new_df.select(all_cols)
        combined_df = existing_df.unionByName(new_df)

        self.spark_connection(combined_df, table_name, mode="overwrite")
            
    def join(self, new_df: DataFrame, table_name: str):
        self.helper_column_creation(new_df, table_name)
        print(f"Union completed and '{table_name}' updated.")
        