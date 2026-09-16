from pyspark.sql import SparkSession

from load.load_to_db import Database_Creation, database_config
from extract.extract import extract_data, kaggle_extract_data
from transform.transform import DataTransformer

def setup():
    def helper_pipeline():
        df = extract_data(local_csv_path)
        transformer = DataTransformer(df)
        cleaned = transformer.get_cleaned_data()
        db.load(cleaned, table_name="chevron_table")

    config, local_csv_path, jar_path = database_config("../../../../config/configs.yaml")

    spark = SparkSession.builder \
        .appName('ChevronETL') \
        .config('spark.jars', jar_path) \
        .getOrCreate()

    db = Database_Creation(spark, config)

    print("Checking if database exist ...")
    not_created = db.create_database_if_not_exists()
    answer = 'y'
    if answer.lower() in ["yes", 'y']:
        helper_pipeline()

        new_data_list = kaggle_extract_data()
        for new_table_name, df in new_data_list:
            transformer = DataTransformer(df)
            transformed = transformer.add_data()
            db.load(transformed, table_name=new_table_name)
        print("Created databases refer to ")
    else:
        print("Skipping additional data")
    # add check if additional data is added. maybe json file that has the datasets used. so question is how do we retain that information?
        print("Database Found: Running pipeline")
        helper_pipeline()
        