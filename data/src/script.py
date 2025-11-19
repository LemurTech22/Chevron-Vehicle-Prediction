from extract import extract_data, kaggle_extract_data
from transform import DataTransformer
from load_to_db import Database_creation, database_config
import pandas as pd
from sqlalchemy import create_engine

def run_etl():
    ans = input("Have you created the database? ")
    db_url, local_csv_path = database_config("../../config/configs.yaml")
    table_name = 'chevron_table'
    
    db = Database_creation(pd.DataFrame(), db_url, table_name)
    db.create_database_if_not_exists()
    
    if ans.lower() in ['no', 'n']:
        
        df = extract_data(local_csv_path)
        transformer = DataTransformer(df)
        transformed_df = transformer.get_cleaned_data()
        db.df = transformed_df
        db.load()
        print("Pipeline completed!")

    else:
        new_data_ans = input("Do you wish to insert more data? (Recommended for first_time use)")
        
        if new_data_ans.lower() in ['yes', 'y']:
            download = input("Do you want to download datasets? ").strip().lower() in ['yes', 'y']
            
            new_data_list = kaggle_extract_data(download)  

            for df in new_data_list:
                transformer = DataTransformer(df)
                transformed_df = transformer.add_data()

                db.join(transformed_df)
                db.load()
            
            print("All new data loaded successfully!")
        else:
            engine = create_engine(db_url)
            query = f"SELECT * FROM {table_name} LIMIT 10;"
            preview_df = pd.read_sql_query(query, engine)

            print(preview_df)
            print("Query Completed")

if __name__ == "__main__":
    run_etl()
