import numpy as np

class DataTransformer:
    def __init__(self, df):
        self.df = df

    def transform_columns(self):
        """Cleaning Dataset"""
        print("Transforming Columns: \n")
        new_columns = [c.strip().lower().replace(" ", "_") for c in self.df.columns]
        self.df = self.df.toDF(*new_columns)
        print(self.df.columns)

    #def replace_na(self):
        """Filling in missing values"""    
      #  print("Filling Missing values")
      #  self.df = self.df.replace(['Not Applicable','Unknown'], np.nan)

    def drop_columns(self):
        print("Dropping Tables: ")
        self.df = self.df.drop('number_of_vehicles_registered_at_the_same_address', 'region')
        print("Columns after Cleaning: {self.df.columns}")

    def drop_unwanted_columns(self):
        """Drops Unnecessary Columns"""
        print("Dropping unwanted columns...")
            #make this dynamic based on correlation factors maybe in data science factor but not in pipeline. 
            #only combine features, rename, or drop obvious features only like postal code, vin, etc...
            #we are trying to predict vehicle trends here.
        columns_to_drop = [
            ]
            
        existing_cols_to_drop = [col for col in columns_to_drop if col in self.df.columns]
        if existing_cols_to_drop:
            print(f"Found {len(existing_cols_to_drop)} columns to drop from {len(self.df.columns)} total columns")

            self.df = self.df.drop(columns=existing_cols_to_drop)

            print(f"Dropped {len(existing_cols_to_drop)} unwanted columns")
            print(f"Remaining columns ({len(self.df.columns)}): {list(self.df.columns)}")
        else:
            print("No columns to drop (all columns are wanted)")
                

    def get_cleaned_data(self):
        self.transform_columns()
        #self.replace_na()
        return self.df

    def add_data(self):
        self.transform_columns()
        #self.replace_na()
        return self.df
    
