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

    def drop_new_data(self):   
        print("Dropping joined tables: ")

        columns_to_drop = ['trim', 'interior','color', 'condition', 'model', 'odometer','seller', 'make', 'body', 'vin',
        'state','mmr', 'transmission', 'quarter', 'county', 'city', 'dol_vehicle_id', 'postal_code','vin_(1-10)', 'legislative_district', 'vehicle_location','tailpipe_co2_ft2',
        'vehicle_id', 'hours_to_charge_120v','start_stop_technology','engine_index', 'transmission_type','annual_consumption_in_barrels_ft2','hatchback_luggage_volume', 'combined_utility_factor',
        'vehicle_charger', 'hours_to_charge_ac_240v','gas_guzzler_tax','engine_descriptor', 'tailpipe_co2_in_grams_mile_ft2','x4d_passenger_volume', ''
        'hours_to_charge_240v','annual_consumption_in_barrels_ft1','manufacturer_code','tailwind_co2_ft1','engine_displacement','supercharger','ghg_score',
        'ghg_score_alt_fuel', 'hatchback_passenger_volume', 'x4d_luggage_volume','x2d_passenger_volume', 'drive', 'x2d_luggage_volume', 'name',
        'description', 'engine','doors', 'exterior_color','interior_color', 'drivetrain']

        print("Columns after Cleaning: {self.df.columns}")
        existing_cols_to_drop = [col for col in columns_to_drop if col in self.df.columns]
        
        if existing_cols_to_drop:
            self.df = self.df.drop(columns=existing_cols_to_drop)
            print(f"Dropped {len(existing_cols_to_drop)} unwanted columns")
            print(f"Remaining columns ({len(self.df.columns)}): {list(self.df.columns)}")

    def get_cleaned_data(self):
        self.transform_columns()
        self.replace_na()
        return self.df

    def add_data(self):
        self.transform_columns()
        self.replace_na()
        return self.df
    