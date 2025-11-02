from sqlalchemy import create_engine
import yaml

class Database_creation:
    def __init__(self, df, url, table_name):
        self.df=df
        self.url = url
        self.table_name = table_name

    def load(self):
        """Loads Dataset into SQL Database"""
        print(f"Loading data into {self.table_name} table ...")

        engine = create_engine(self.url)

        self.df.to_sql(self.table_name,engine, if_exists="replace")
        
        print("Data loaded into Database Successfully! ")
        
    def get_db(self):
        self.load()
        return self.df
    
def database_config(url):
    with open(url, "r") as f:
        config=yaml.safe_load(f)
        print("Config", config, type(config))
    
    path="chevron_data.csv"
    
    return config["database_url"],path
