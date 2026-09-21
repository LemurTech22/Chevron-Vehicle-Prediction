from logs.logger import ErrorCategory, ETL_Logger

from urllib.parse import urlparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import col as spark_col, lit
import os
import yaml
from dotenv import load_dotenv
from yaml_env_tag import add_env_tag

_Loader = add_env_tag(yaml.SafeLoader)


def database_config(config_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.abspath(os.path.join(base_dir, config_path))
    project_root = os.path.dirname(os.path.dirname(full_path))

    # .env is expected at the project root; adjust if yours lives elsewhere
    load_dotenv(os.path.join(project_root, ".env"))

    with open(full_path, "r") as f:
        config = yaml.load(f, Loader=_Loader)

    csv_path = os.path.join(project_root, config["csv_path"])
    jar_path = os.path.join(project_root, config["postgres_jar_path"])

    log = ETL_Logger(ErrorCategory.DATABASE)
    log.info("Opening Configuration File")
    log.info(f"Loaded Config: {config}")
    log.info(f"Loaded CSV path: {csv_path}")
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
        self.log = ETL_Logger(ErrorCategory.DATABASE)

    def create_database_if_exists(self):
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
            cur.execute(f"CREATE DATABASE {self.db_name}")
            self.log.info(f"Created DATABASE: {self.db_name}")
        else:
            self.log.info(f"Database: {self.db_name} already exists.")

        cur.close()
        conn.close()

    def spark_connection(self, df: DataFrame, table_name: str, mode: str):
        self.log.info(f"Loading Spark Dataframe/SQL into '{table_name}' and '{mode}' to the Table.")
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
            self.log.info("Write Complete")
        elif mode == "read":
            result_df = self.spark.read \
                .format("jdbc") \
                .option("url", self.db_url) \
                .option("dbtable", table_name) \
                .options(**properties) \
                .load()
            self.log.info(f"Reading: {table_name}")
            return result_df
        else:
            self.log.error(f"Database feature: {mode} is unavailable")
            self.log.error(f"Expected append, overwrite, read")
            self.log.error(f"Refer to spark_connection function.")
            raise ValueError(f"{mode} feature is unavailable. \n Expected: append, overwrite, read")

    def load(self, df: DataFrame, table_name: str, mode="append"):
        self.log.info(f"Loading Spark Dataframe into {table_name} ...")
        self.spark_connection(df, table_name, mode)

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
        self.log.info(f"Union completed and {table_name} updated.")
        