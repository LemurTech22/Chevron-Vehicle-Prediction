import yaml
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from urllib.parse import urlparse
import os

class Database_creation:
    def __init__(self, df, db_url, table_name):
        self.df = df
        self.db_url = db_url
        self.table_name = table_name

    def create_database_if_not_exists(self):
        """Creates the PostgreSQL database if it doesn't exist"""
        try:

            parsed = urlparse(self.db_url)
            db_name = parsed.path.lstrip('/')
            user = parsed.username
            password = parsed.password
            host = parsed.hostname
            port = parsed.port or 5432

            conn = psycopg2.connect(
                dbname="postgres",
                user=user,
                password=password,
                host=host,
                port=port
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()

            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
            exists = cur.fetchone()

            if not exists:
                cur.execute(f'CREATE DATABASE "{db_name}";')
                print(f"✅ Database '{db_name}' created successfully!")
            else:
                print(f"ℹ️ Database '{db_name}' already exists.")

            cur.close()
            conn.close()

        except Exception as e:
            print("Error creating database:", e)

    def load(self):
        """Loads Dataset into PostgreSQL Database"""
        print(f"Loading data into {self.table_name} table ...")
        try:
            engine = create_engine(self.db_url)
            """change if_exists whether we want to add data or make a new database. Append adds data while replace makes a new database using the new data."""
            self.df.to_sql(
                self.table_name,
                engine,
                if_exists="append",
                index=False
            )

            print("Data loaded into PostgreSQL successfully!")

        except SQLAlchemyError as e:
            print("Database load failed:", e)

    def get_db(self):
        self.create_database_if_not_exists()
        self.load()
        return self.df


def database_config(config_path):
    """Reads database configuration from YAML"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path= os.path.join(base_dir, config_path)

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        print("Config loaded:", config, type(config))
    
    path = os.path.join(base_dir, "Chevron_data.csv")
    print(config, path)

    return config["database_url"],path
