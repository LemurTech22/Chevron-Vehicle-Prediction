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

    def drop_unwanted_columns(self):
        """Drops Unnecessary Columns"""
        print("Dropping unwanted columns...")
            #make this dynamic based on correlation factors maybe in data science factor but not in pipeline. 
            #only combine features, rename, or drop obvious features only like postal code, vin, etc...
            #we are trying to predict vehicle trends here.
        columns_to_drop = [
                'trim', 'interior', 'color', 'condition', 'model', 'odometer', 'seller', 
                'make', 'body', 'vin', 'state', 'mmr', 'transmission', 'quarter', 'county', 
                'city', 'dol_vehicle_id', 'postal_code', 'vin_(1-10)', 'legislative_district', 
                'vehicle_location', 'tailpipe_co2_ft2', 'vehicle_id', 'hours_to_charge_120v',
                'start_stop_technology', 'engine_index', 'transmission_type',
                'annual_consumption_in_barrels_ft2', 'hatchback_luggage_volume', 
                'combined_utility_factor', 'vehicle_charger', 'hours_to_charge_ac_240v',
                'gas_guzzler_tax', 'engine_descriptor', 'tailpipe_co2_in_grams_mile_ft2',
                'x4d_passenger_volume', 'hours_to_charge_240v', 
                'annual_consumption_in_barrels_ft1', 'manufacturer_code', 
                'tailpipe_co2_ft1', 'engine_displacement', 'supercharger', 'ghg_score',
                'ghg_score_alt_fuel', 'hatchback_passenger_volume', 'x4d_luggage_volume',
                'x2d_passenger_volume', 'drive', 'x2d_luggage_volume', 'name', 
                'description', 'engine', 'doors', 'exterior_color', 'interior_color', 
                'drivetrain', 'saledate', 'sellingprice', 'sales', 'base_msrp', 
                'electric_range', 'clean_alternative_fuel_vehicle_(cafv)_eligibility',
                'electric_vehicle_type', '2020_census_tract', 'electric_utility',
                'price', 'mileage', 'cylinders', 'fuel', 'type', 'year',
                'tailpipe_co2_in_grams_mile_ft1', 'fuel_economy_score', 'my_mpg_data',
                'alternative_fuel_technology', 'electric_motor', 'gasoline_electricity_blended_cd',
                'alternate_charger', 'composite_city_mpg', 'composite_highway_mpg',
                'composite_combined_mpg', 'range_ft1', 'city_range_ft1', 'highway_range_ft1',
                'range_ft2', 'city_range_ft2', 'highway_range_ft2', 'save_or_spend_5_year',
                'class', 'unadjusted_city_mpg_ft1', 'unadjusted_highway_mpg_ft1',
                'unadjusted_city_mpg_ft2', 'unadjusted_highway_mpg_ft2',
                'combined_mpg_ft1', 'unrounded_combined_mpg_ft1', 'combined_mpg_ft2',
                'unrounded_combined_mpg_ft2', 'combined_electricity_consumption',
                'combined_gasoline_consumption_cd', 'annual_fuel_cost_ft1', 
                'annual_fuel_cost_ft2', 'city_mpg_ft1', 'unrounded_city_mpg_ft1',
                'city_mpg_ft2', 'unrounded_city_mpg_ft2', 'city_gasoline_consumption_cd',
                'city_electricity_consumption', 'city_utility_factor', 'highway_mpg_ft1',
                'unrounded_highway_mpg_ft1', 'highway_mpg_ft2', 'unrounded_highway_mpg_ft2',
                'highway_gasoline_consumption_cd', 'highway_electricity_consumption',
                'highway_utility_factor', 'fuel_type_1', 'fuel_type_2',
                'engine_cylinders', 'turbocharger', 'doors', 'name', 'vehicle_id', 
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
        self.replace_na()
        return self.df

    def add_data(self):
        self.transform_columns()
        self.replace_na()
        return self.df
    
