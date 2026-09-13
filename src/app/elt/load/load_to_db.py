from urllib.parse import urlparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
import os, yaml


# Standalone function — no self needed, no chicken-and-egg problem
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
    def __init__(self, spark: SparkSession, df: DataFrame, config: dict, table_name: str):
        self.spark = spark
        self.df = df
        self.table_name = table_name

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

    def load(self, mode="append"):
        print(f"Loading Spark DataFrame into '{self.table_name}'...")
        properties = {
            "user": self.user,
            "password": self.password,
            "driver": "org.postgresql.Driver"
        }
        self.df.write \
            .format("jdbc") \
            .option("url", self.db_url) \
            .option("dbtable", self.table_name) \
            .options(**properties) \
            .mode(mode) \
            .save()
        print("Load complete.")

    def join(self, new_df: DataFrame):
        existing_df = self.spark.read \
            .format("jdbc") \
            .option("url", self.db_url) \
            .option("dbtable", self.table_name) \
            .option("driver", "org.postgresql.Driver") \
            .options(user=self.user, password=self.password) \
            .load()

        existing_cols = existing_df.columns
        new_cols = new_df.columns
        all_cols = list(set(existing_cols) | set(new_cols))

        for col in all_cols:
            if col not in existing_cols:
                existing_df = existing_df.withColumn(col, lit(None))
            if col not in new_cols:
                new_df = new_df.withColumn(col, lit(None))

        existing_df = existing_df.select(all_cols)
        new_df = new_df.select(all_cols)
        self.df = existing_df.unionByName(new_df)
        print("Union completed.")