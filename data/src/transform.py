import numpy as np

class DataTransformer:
    def __init__(self,df):
        self.df = df

    def transform_columns(self):
        """Cleaning Dataset"""

        print("Cleaning Dataset: \n")

        self.df.columns = [c.strip().lower().replace(" ", "_") for c in self.df.columns]

        print(self.df.columns)

    def replace_na(self):
        """Filling in missing values"""
            
        print("Filling Missing values")

        self.df = self.df.replace(['Not Applicable','Unknown'], np.nan)

    def drop_columns(self):
        print("Dropping Tables: ")
        self.df.drop(columns=['number_of_vehicles_registered_at_the_same_address', 'region'])
        print("Columns after Cleaning: {self.df.columns}")

    def get_cleaned_data(self):
        self.transform_columns()
        self.replace_na()
        return self.df
