import re
import numpy as np
from logs.logger import ETL_Logger, ErrorCategory
from pyspark.sql.functions import col, when

class DataTransformer:
    def __init__(self, df):
        self.df = df
        self.log = ETL_Logger(ErrorCategory.GENERAL)

    def transform_columns(self):
        self.log.info("Cleaning Dataset -- normalize every column name into a safe, unquoted SQL identifier.")
        self.log.info("Transforming Columns: ")
        print("Transforming Columns: \n")

        new_columns = []
        for c in self.df.columns:
            clean = c.strip().lower()
            clean = re.sub(r"[^a-z0-9]+", "_", clean)   # anything not a letter/digit -> underscore
            clean = clean.strip("_")                     # trim leading/trailing underscores
            if clean and clean[0].isdigit():              # SQL identifiers can't start with a digit
                clean = f"col_{clean}"
            new_columns.append(clean)

        self.df = self.df.toDF(*new_columns)
        
        for col_name in self.df.columns:
            self.df = self.df.withColumn(col_name, self.df[col_name].cast(("string")))
        print(self.df.columns)

    def replace_na(self):
        """Filling in missing values"""
        self.log.info("Filling in missing values.")
        print("Filling Missing values")
        
        replacement_values = ['Not Applicable', 'Unknown']
        for column in self.df.columns:
            if self.df.schema[column].dataType.simpleString() == "string":
                self.df = self.df.withColumn(
                    column,
                    when(col(column).isin(replacement_values), None).otherwise(col(column))
                )

    def drop_duplicates(self):
        print(f"Dropping duplicates for {self.df.columns}")
        self.log.info(f"Dropping duplicates for {self.df.columns}")
        self.df = self.df.dropDuplicates()
        
    def drop_unwanted_columns(self):
        """Drops Unnecessary Columns"""
        print("Dropping unwanted columns...")
        columns_to_drop = [
        ]
        existing_cols_to_drop = [col for col in columns_to_drop if col in self.df.columns]
        if existing_cols_to_drop:
            print(f"Found {len(existing_cols_to_drop)} columns to drop from {len(self.df.columns)} total columns")
            self.df = self.df.drop(*existing_cols_to_drop)
            print(f"Dropped {len(existing_cols_to_drop)} unwanted columns")
            print(f"Remaining columns ({len(self.df.columns)}): {list(self.df.columns)}")
        else:
            print("No columns to drop (all columns are wanted)")

    def get_cleaned_data(self):
        self.transform_columns()
        self.replace_na()
        self.drop_duplicates()
        return self.df
