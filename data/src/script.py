from extract import extract_data
from transform import DataTransformer
from load_to_db import Database_creation, database_config
from sqlalchemy import create_engine
import pandas as pd

def run_etl():
    ans = input("Have you created the database? ")

    if(ans.lower() in ['no', 'n']):
        config,file_path = database_config("../../config/configs.yaml")

        df = extract_data(file_path)

        transformer = DataTransformer(df)
        transformed = transformer.get_cleaned_data()

        db = Database_creation(transformed, config, 'chevron_table')
        db.get_db()
        print("Pipeline completed!")

    else:
        db_url,_ = database_config("../../config/configs.yaml")
        engine = create_engine(db_url)

        query= "SELECT * FROM chevron_table LIMIT 5;"
        df = pd.read_sql_query(query, engine)

        print(df)
        print("Query Completed")
    
if  __name__ == "__main__":
    run_etl()
