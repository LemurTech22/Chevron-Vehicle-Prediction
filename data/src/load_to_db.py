import yaml
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from urllib.parse import urlparse
import os
import pandas as pd

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
                dbname=db_name,
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
                print(f"Database '{db_name}' created successfully!")
            else:
                print(f"Database '{db_name}' already exists.")

            cur.close()
            conn.close()

        except Exception as e:
            print("Error creating database:", e)
    
    def add_new_columns_to_table(self, new_columns):
        """Adds new columns to the database table if they don't exist"""
        try:
            engine = create_engine(self.db_url)
            inspector = inspect(engine)
            
            if inspector.has_table(self.table_name):
                # Get existing columns in the table
                existing_columns = [col['name'] for col in inspector.get_columns(self.table_name)]
                
                # Find columns that need to be added
                columns_to_add = [col for col in new_columns if col not in existing_columns]
                
                if columns_to_add:
                    print(f"Adding {len(columns_to_add)} new columns to the table...")
                    
                    with engine.connect() as conn:
                        for col in columns_to_add:
                            # Add column as TEXT type
                            alter_query = text(f'ALTER TABLE {self.table_name} ADD COLUMN IF NOT EXISTS "{col}" TEXT')
                            conn.execute(alter_query)
                        conn.commit()
                    
                    print(f"Successfully added {len(columns_to_add)} new columns!")
                else:
                    print("No new columns to add.")
        except Exception as e:
            print(f"Error adding new columns: {e}")
    
    def column_alignment(self, df):
        """Aligns DataFrame columns with existing table schema"""
        try:
            engine = create_engine(self.db_url)
            inspector = inspect(engine)
            
            # Check if table exists
            if inspector.has_table(self.table_name):
                # Get existing columns
                existing_columns = [col['name'] for col in inspector.get_columns(self.table_name)]
                
                # Add missing columns to DataFrame that exist in table (with None values)
                for col in existing_columns:
                    if col not in df.columns:
                        df[col] = None
                
                # Reorder DataFrame to match table column order
                df = df[existing_columns]
                
                print(f"Aligned DataFrame with table schema. Columns: {len(existing_columns)}")
            
            return df
        except Exception as e:
            print(f"Error aligning columns: {e}")
            return df
            
    def drop_unwanted_columns(self):
        """Drops columns we don't want to keep in the database"""
        print("Dropping unwanted columns...")
        
        columns_to_drop = [
            'trim', 'interior', 'color', 'condition', 'model', 'odometer', 'seller', 
            'make', 'body', 'vin', 'state', 'mmr', 'transmission', 'quarter', 'county', 
            'city', 'dol_vehicle_id', 'postal_code', 'vin_(1-10)', 'legislative_district', 
            'vehicle_location', 'tailpipe_co2_ft2', 'vehicle_id', 'hours_to_charge_120v',
            'start_stop_technology', 'engine_index', 'transmission_type',
            'annual_consumption_in_barrels_ft2', 'hatchback_luggage_volume', 
            'combined_utility_factor', 'vehicle_charger', 'hours_to_charge_ac_240v',
            'gas_guzzler_tax', 'engine_descriptor', 'tailpipe_co2_in_grams_mile_ft2',
            'x4d_passenger_volume', 'hours_to_charge_240v', 
            'annual_consumption_in_barrels_ft1', 'manufacturer_code', 
            'tailpipe_co2_ft1', 'engine_displacement', 'supercharger', 'ghg_score',
            'ghg_score_alt_fuel', 'hatchback_passenger_volume', 'x4d_luggage_volume',
            'x2d_passenger_volume', 'drive', 'x2d_luggage_volume', 'name', 
            'description', 'engine', 'doors', 'exterior_color', 'interior_color', 
            'drivetrain', 'saledate', 'sellingprice', 'sales', 'base_msrp', 
            'electric_range', 'clean_alternative_fuel_vehicle_(cafv)_eligibility',
            'electric_vehicle_type', '2020_census_tract', 'electric_utility',
            'price', 'mileage', 'cylinders', 'fuel', 'type', 'year',
            'tailpipe_co2_in_grams_mile_ft1', 'fuel_economy_score', 'my_mpg_data',
            'alternative_fuel_technology', 'electric_motor', 'gasoline_electricity_blended_cd',
            'alternate_charger', 'composite_city_mpg', 'composite_highway_mpg',
            'composite_combined_mpg', 'range_ft1', 'city_range_ft1', 'highway_range_ft1',
            'range_ft2', 'city_range_ft2', 'highway_range_ft2', 'save_or_spend_5_year',
            'class', 'unadjusted_city_mpg_ft1', 'unadjusted_highway_mpg_ft1',
            'unadjusted_city_mpg_ft2', 'unadjusted_highway_mpg_ft2',
            'combined_mpg_ft1', 'unrounded_combined_mpg_ft1', 'combined_mpg_ft2',
            'unrounded_combined_mpg_ft2', 'combined_electricity_consumption',
            'combined_gasoline_consumption_cd', 'annual_fuel_cost_ft1', 
            'annual_fuel_cost_ft2', 'city_mpg_ft1', 'unrounded_city_mpg_ft1',
            'city_mpg_ft2', 'unrounded_city_mpg_ft2', 'city_gasoline_consumption_cd',
            'city_electricity_consumption', 'city_utility_factor', 'highway_mpg_ft1',
            'unrounded_highway_mpg_ft1', 'highway_mpg_ft2', 'unrounded_highway_mpg_ft2',
            'highway_gasoline_consumption_cd', 'highway_electricity_consumption',
            'highway_utility_factor', 'fuel_type_1', 'fuel_type_2',
            'engine_cylinders', 'turbocharger'
        ]
        
        # Only drop columns that actually exist in the DataFrame
        existing_cols_to_drop = [col for col in columns_to_drop if col in self.df.columns]
        
        if existing_cols_to_drop:
            print(f"Found {len(existing_cols_to_drop)} columns to drop from {len(self.df.columns)} total columns")
            self.df = self.df.drop(columns=existing_cols_to_drop)
            print(f"Dropped {len(existing_cols_to_drop)} unwanted columns")
            print(f"Remaining columns ({len(self.df.columns)}): {list(self.df.columns)}")
        else:
            print("No columns to drop (all columns are wanted)")
    
    def load(self):
        """Loads Dataset into PostgreSQL Database"""
        print(f"Loading data into {self.table_name} table ...")
        if self.df is not None and not self.df.empty:
            try:
                # Drop unwanted columns BEFORE loading
                self.drop_unwanted_columns()
                
                engine = create_engine(self.db_url)
                inspector = inspect(engine)

                if inspector.has_table(self.table_name):
                    # FIRST: Add any new columns from this DataFrame to the table
                    self.add_new_columns_to_table(self.df.columns.tolist())
                    
                    # THEN: Align DataFrame to match the updated table schema
                    self.df = self.column_alignment(self.df)
                    if_exists_mode = "append"
                else:
                    if_exists_mode = "replace"
                    print(f"Creating new table with {len(self.df.columns)} columns")
                
                self.df.to_sql(
                    self.table_name,
                    engine,
                    if_exists=if_exists_mode,
                    index=False
                )

                print(f"Data loaded into PostgreSQL successfully! ({len(self.df)} rows)")

            except SQLAlchemyError as e:
                print("Database load failed:", e)
        
    def join(self, new_df):
        """Joins new data with existing data in memory before loading"""
        print(f"Joining Data to {self.table_name}")
        try:
            engine = create_engine(self.db_url)
            
            # Read existing table
            existing_df = pd.read_sql_table(self.table_name, engine)
            
            # Combine all columns from both DataFrames
            all_columns = list(set(existing_df.columns) | set(new_df.columns))
            
            # Add missing columns to both DataFrames
            for col in all_columns:
                if col not in existing_df.columns:
                    existing_df[col] = None
                if col not in new_df.columns:
                    new_df[col] = None
            
            # Ensure column order matches
            existing_df = existing_df[all_columns]
            new_df = new_df[all_columns]
            
            # Concatenate
            self.df = pd.concat([existing_df, new_df], ignore_index=True)
            self.df.drop_duplicates(inplace=True)
            
            print(f"Joined {len(new_df)} new rows with {len(existing_df)} existing rows")
            print(f"Total rows after deduplication: {len(self.df)}")
        except Exception as e:
            print(f"No existing data to join, using new data only: {e}")
            self.df = new_df
        
    def get_db(self):
        self.create_database_if_not_exists()
        self.load()
        return self.df


def database_config(config_path):
    """Reads database configuration from YAML"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, config_path)

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        print("Config loaded:", config, type(config))
    
    path = os.path.join(base_dir, "Chevron_data.csv")
    print(config, path)

    return config["database_url"], path
