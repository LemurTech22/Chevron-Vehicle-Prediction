from pyspark.sql import SparkSession
from pyspark.sql.functions import sha2, struct, to_json

from pipeline.load.load_to_db import Database_Creation, database_config
from pipeline.extract.extract import extract_data, kaggle_extract_data
from pipeline.transform.transform import DataTransformer

from scripts.dbt.run_dbt_build import run_dbt_build
from scripts.db.export_db import database_export
from logs.logger import ETL_Logger, ErrorCategory


TABLE_KEYS = {
    "chevron_table": [
        "date", "vehicle_category", "gvwr_class", "fuel_type", "model_year",
        "fuel_technology", "electric_mile_range",
        "number_of_vehicles_registered_at_the_same_address", "region",
    ],
    "raw_ev_population": ["_row_hash"],
    "raw_vehicle_sales": ["_row_hash"],
    "raw_fuel_economy": ["_row_hash"],
}

HASH_KEYED_TABLES = {"raw_ev_population", "raw_vehicle_sales", "raw_fuel_economy"}


def add_row_hash(df):
    """Add a deterministic SHA-256 hash for each row's transformed values."""
    row_columns = [column for column in df.columns if column != "_row_hash"]
    return df.withColumn("_row_hash", sha2(to_json(struct(*row_columns)), 256))

def _load_dataset(db, df, table_name: str, transform_method: str):
    transformer = DataTransformer(df)
    transformed = getattr(transformer, transform_method)()

    if table_name in HASH_KEYED_TABLES:
        transformed = add_row_hash(transformed)

    key_cols = TABLE_KEYS.get(table_name)
    missing = [c for c in (key_cols or []) if c not in transformed.columns]
    if missing:
        raise ValueError(
            f"{table_name}: key_cols {missing} not in transformed schema "
            f"{transformed.columns}. TABLE_KEYS is stale."
        )

    db.join(transformed, table_name=table_name, key_cols=key_cols)
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
    log.info("Checking if env's exists")
    db.require_env_var("KAGGLE_API_TOKEN", "DB_HOST", "DB_USER", "DB_PASSWORD", "DB_PORT", "DB_NAME", "OUTPUT_DIR")
    log.info("Checking if database exists ...")
    db.create_database_if_exists()

    helper_pipeline(db, local_csv_path)
    helper_dbt()


def database_setup():
    setup()