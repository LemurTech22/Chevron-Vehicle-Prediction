from pyspark.sql import SparkSession

from pipeline.load.load_to_db import Database_Creation, database_config
from pipeline.extract.extract import extract_data, kaggle_extract_data
from pipeline.transform.transform import DataTransformer

from scripts.dbt.run_dbt_build import run_dbt_build
from scripts.db.export_db import database_export
from logs.logger import ETL_Logger, ErrorCategory


def helper_pipeline(db, local_csv_path):
    df = extract_data(local_csv_path)
    transformer = DataTransformer(df)
    cleaned = transformer.get_cleaned_data()
    db.load(cleaned, table_name="chevron_table")

    new_data_list = kaggle_extract_data()
    for new_table_name, df in new_data_list:
        transformer = DataTransformer(df)
        transformed = transformer.add_data()
        db.load(transformed, table_name=new_table_name)
        print(f"Loaded {new_table_name}")


def helper_dbt():
    log = ETL_Logger(ErrorCategory.VALIDATION)
    dbt_result = run_dbt_build(project_dir="dbt_project", profile_dir="dbt_project")

    if dbt_result.success:
        log = ETL_Logger(ErrorCategory.DATABASE)
        log.info("Exporting Stage 1 Database")
        database_export("staging_1").db_export_script()
    else:
        log = ETL_Logger(ErrorCategory.VALIDATION)
        log.error("DBT failed to validate schema for final staging; staging folder was rolled back.")
        log.debug("Check schema in final dbt run. pipeline/VALIDATION/validation_error.log")
        raise ValueError("DBT failed to validate schema on final staging.")


def setup():
    config_path = "../../../config/configs.yaml"
    config, local_csv_path, jar_path = database_config(config_path)

    spark = SparkSession.builder \
        .appName('ChevronETL') \
        .config('spark.jars', jar_path) \
        .getOrCreate()

    db = Database_Creation(spark, config)
    log = ETL_Logger(ErrorCategory.DATABASE)
    log.info("Checking if database exists ...")
    db.create_database_if_exists()

    helper_pipeline(db, local_csv_path)
    helper_dbt()


def database_setup():
    setup()