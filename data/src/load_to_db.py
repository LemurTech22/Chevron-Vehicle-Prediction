import yaml
from sqlalchemy import create_engine, inspect, text
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from urllib.parse import urlparse
import os
from transform import DataTransformer
import pandas as pd

def database_config(config_path):
    """Reads database configuration from YAML"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, config_path)

    with open(full_path, "r") as f:
        config = yaml.safe_load(f)

    # Load local CSV path inside data folder
    csv_path = os.path.join(base_dir, "Chevron_data.csv")

    print("Loaded config:", config)
    print("Loaded CSV path:", csv_path)

    return config["database_url"], csv_path

class Database_creation:
    def __init__(self, df, db_url, table_name):
        transformer = DataTransformer(df)
        self.df = transformer.get_cleaned_data()
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

    def add_new_columns_to_table(self):
        engine = create_engine(self.db_url)
        inspector = inspect(engine)

        if not inspector.has_table(self.table_name):
            return

        existing_cols = [c["name"] for c in inspector.get_columns(self.table_name)]
        new_cols = [c for c in self.df.columns if c not in existing_cols]

        if not new_cols:
            print("No new columns needed.")
            return

        print(f"Adding {len(new_cols)} new columns...")
        with engine.connect() as conn:
            for col in new_cols:
                conn.execute(text(
                    f'ALTER TABLE "{self.table_name}" ADD COLUMN "{col}" TEXT'
                ))
            conn.commit()

    def align_columns(self):
        engine = create_engine(self.db_url)
        inspector = inspect(engine)

        if not inspector.has_table(self.table_name):
            return self.df

        db_cols = [col["name"] for col in inspector.get_columns(self.table_name)]

        for col in db_cols:
            if col not in self.df.columns:
                self.df[col] = None

        self.df = self.df[db_cols]
        return self.df
    
    def join(self, new_df):
        """Join new data with existing table data in memory before loading"""
        print(f"Joining new data to '{self.table_name}'")
        engine = create_engine(self.db_url)
        inspector = inspect(engine)

        if inspector.has_table(self.table_name):
            existing_df = pd.read_sql_table(self.table_name, engine)

            all_cols = list(set(existing_df.columns) | set(new_df.columns))
            for col in all_cols:
                if col not in existing_df.columns:
                    existing_df[col] = None
                if col not in new_df.columns:
                    new_df[col] = None

            existing_df = existing_df[all_cols]
            new_df = new_df[all_cols]

            self.df = pd.concat([existing_df, new_df], ignore_index=True)
            self.df.drop_duplicates(inplace=True)
            print(f"Joined {len(new_df)} rows with existing {len(existing_df)} rows")
        else:
            self.df = new_df
            print("Table doesn't exist yet; using new data as initial dataset")

    def load(self):
        print(f"Loading data into table '{self.table_name}'...")

        engine = create_engine(self.db_url)
        inspector = inspect(engine)
        exists = inspector.has_table(self.table_name)

        if exists:
            self.add_new_columns_to_table()
            self.df = self.align_columns()
            mode = "append"
        else:
            print("Creating table for the first time...")
            mode = "replace"

        self.df.to_sql(self.table_name, engine, if_exists=mode, index=False)
        print(f"Loaded {len(self.df)} rows.")

    def get_db(self):
        self.create_database_if_not_exists()
        self.load()
        return self.df
