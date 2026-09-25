from pyspark.sql import SparkSession

from pipeline.load.load_to_db import Database_Creation, database_config
from pipeline.extract.extract import extract_data, kaggle_extract_data
from pipeline.transform.transform import DataTransformer

from scripts.dbt.run_dbt_build import run_dbt_build
from scripts.db.export_db import database_export
from logs.logger import ETL_Logger, ErrorCategory


def _load_dataset(db, df, table_name: str, transform_method: str):
    transformer = DataTransformer(df)
    transformed = getattr(transformer, transform_method)()
    db.load(transformed, table_name=table_name)
    print(f"Loaded {table_name}")


def helper_pipeline(db, local_csv_path):
    chevron_df = extract_data(local_csv_path)
    kaggle_data = kaggle_extract_data()

    datasets = [("chevron_table", chevron_df, "get_cleaned_data")]
    datasets += [(table_name, df, "get_cleaned_data") for table_name, df in kaggle_data]

    for table_name, df, transform_method in datasets:
        _load_dataset(db, df, table_name, transform_method)


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
    
    #env check
    log.info("Checking if env's exists")
    db.require_env_var("KAGGLE_API_TOKEN","DB_HOST", "DB_USER", "DB_PASSWORD", "DB_PORT", "DB_NAME", "OUTPUT_DIR")
    
    log.info("Checking if database exists ...")
    db.create_database_if_exists()

    helper_pipeline(db, local_csv_path)
    helper_dbt()


def database_setup():
    setup()