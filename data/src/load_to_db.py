from urllib.parse import urlparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
import os, yaml  # noqa: E401


def database_config(config_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, config_path)

    with open(full_path, "r") as f:
        config = yaml.safe_load(f)

    csv_path = os.path.join(base_dir, "Chevron_data.csv")

    print("Loaded config:", config)
    print("Loaded CSV path:", csv_path)

    return config["database_url"], csv_path
class Database_Creation:
    def __init__(self, spark: SparkSession, df: DataFrame, db_url: str, table_name: str):
        self.spark = spark
        self.df = df
        self.db_url = db_url
        self.table_name = table_name

    def create_database_if_not_exists(self):
        parsed = urlparse(self.db_url)
        db_name = parsed.path.lstrip("/")
        user = parsed.username
        pwd = parsed.password
        host = parsed.hostname
        port = parsed.port or 5432

        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=pwd,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cur.fetchone()

        if not exists:
            cur.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Created database: {db_name}")
        else:
            print(f"Database {db_name} already exists")

        cur.close()
        conn.close()

    def load(self, mode="append"):
        print(f"Loading Spark DataFrame into '{self.table_name}'...")

        properties = {
            "user": urlparse(self.db_url).username,
            "password": urlparse(self.db_url).password,
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

    # ----------------------------------------
    # Merge (UNION) new Spark DataFrame
    # ----------------------------------------
    def join(self, new_df: DataFrame):
        print("Unioning new Spark DF with existing table data...")

        # Load existing table
        existing_df = self.spark.read \
            .format("jdbc") \
            .option("url", self.db_url) \
            .option("dbtable", self.table_name) \
            .option("driver", "org.postgresql.Driver") \
            .load()

        # Align columns
        existing_cols = existing_df.columns
        new_cols = new_df.columns

        all_cols = list(set(existing_cols) | set(new_cols))

        # Add missing columns
        for col in all_cols:
            if col not in existing_cols:
                existing_df = existing_df.withColumn(col, lit(None))

            if col not in new_cols:
                new_df = new_df.withColumn(col, lit(None))

        # Same column order
        existing_df = existing_df.select(all_cols)
        new_df = new_df.select(all_cols)

        # Union
        self.df = existing_df.unionByName(new_df)
        print("Union completed.")
