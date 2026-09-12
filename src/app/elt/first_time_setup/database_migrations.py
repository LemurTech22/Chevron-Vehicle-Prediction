from pyspark.sql import SparkSession

from load.load_to_db import Database_Creation, database_config
from extract.extract import extract_data, kaggle_extract_data
from transform.transform import DataTransformer

def setup():
    def helper_pipeline():
        df = extract_data(local_csv_path)
        db.df = df
        db.load()

    config, local_csv_path, jar_path = database_config("../../../../config/configs.yaml")

    spark = SparkSession.builder \
        .appName('ChevronETL') \
        .config('spark.jars', jar_path) \
        .getOrCreate()

    table_name = 'chevron_table'
    db = Database_Creation(spark, None, config, table_name)

    print("Checking if database exist ...")
    not_created = db.create_database_if_not_exists()

    if not_created:
        helper_pipeline()
        ans = input("Do you wish to insert more data?")
        if ans.lower() in ['yes', 'y']:
            new_data_list = kaggle_extract_data()
            for df in new_data_list:
                transformer = DataTransformer(df)
                transformed = transformer.add_data(transformer)
                db.join(transformed)
                db.save()
        else:
            print("Skipping additional data")
    else:
        print("Database Found: Running pipeline")
        helper_pipeline()