from pyspark.sql import SparkSession

from load.load_to_db import Database_Creation, database_config
from extract.extract import extract_data, kaggle_extract_data
from transform.transform import DataTransformer

from scripts.dbt.run_dbt_build import run_dbt_build
from scripts.db.export_db import database_export

def setup():
    def helper_dbt():
        dbt_result = run_dbt_build(project_dir="dbt_project", profile_dir="dbt_project")
        if dbt_result.success:
            database_export("staging_1").db_export_script()
        else:
            raise ValueError("DBT Failed to validate schema on final staging.")

    def helper_pipeline():
        # Local CSV -> chevron_table, every run.
        df = extract_data(local_csv_path)
        transformer = DataTransformer(df)
        cleaned = transformer.get_cleaned_data()
        db.load(cleaned, table_name="chevron_table")

        # Kaggle datasets, every run -- kaggle_extract_data() already skips
        # unchanged datasets internally via its own timestamp check.
        new_data_list = kaggle_extract_data()
        for new_table_name, df in new_data_list:
            transformer = DataTransformer(df)
            transformed = transformer.add_data()
            db.load(transformed, table_name=new_table_name)
            print(f"Loaded {new_table_name}")

    config, local_csv_path, jar_path = database_config("../../../../config/configs.yaml")

    spark = SparkSession.builder \
        .appName('ChevronETL') \
        .config('spark.jars', jar_path) \
        .getOrCreate()

    db = Database_Creation(spark, config)

    print("Checking if database exists ...")
    db.create_database_if_exists() 
    helper_pipeline()
    helper_dbt()