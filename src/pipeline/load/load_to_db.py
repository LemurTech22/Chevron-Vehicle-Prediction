from logs.logger import ErrorCategory, ETL_Logger

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
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

    def require_env_var(self, *names:str) -> dict:
        load_dotenv()
        log = ETL_Logger(ErrorCategory.VALIDATION)

        all_present = True
        for name in names:
            value = os.environ.get(name)
            if value is None or value.strip() == "":
                log.error(f"Missing required environment variable: {name}")
                all_present = False
        if not all_present:
            raise EnvironmentError("One or more required environment variables are missing. Check the errors above.")
        else: 
            log.info("All environment variables exists moving onto pipeline.")


    def table_exists(self, table_name: str) -> bool:
            conn = psycopg2.connect(
                dbname=self.db_name, user=self.user, password=self.password,
                host=self.host, port=self.port
            )
            cur = conn.cursor()
            cur.execute(
                "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)",
                (table_name,)
            )
            exists = cur.fetchone()[0]
            cur.close()
            conn.close()
            return exists
    
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

    def join(self, new_df: DataFrame, table_name: str, key_cols: list):
        if not key_cols:
            raise ValueError(f"key_cols is required for {table_name}.")

        new_df = new_df.dropDuplicates(key_cols)

        if not self.table_exists(table_name):
            self.log.info(f"{table_name} does not exist yet — initial load.")
            self.load(new_df, table_name, mode="append")
            return

        existing_keys = self.spark_connection(None, table_name, mode="read") \
            .select(*key_cols).distinct()

        join_condition = None
        for k in key_cols:
            cond = new_df[k].eqNullSafe(existing_keys[k])
            join_condition = cond if join_condition is None else (join_condition & cond)

        to_insert = new_df.join(existing_keys, on=join_condition, how="left_anti") \
                        .select(new_df["*"])

        inserted_count = to_insert.count()
        if inserted_count == 0:
            self.log.info(f"{table_name}: no new rows to insert.")
            return

        self.load(to_insert, table_name, mode="append")
        self.log.info(f"{table_name}: inserted {inserted_count} new row(s).")
        