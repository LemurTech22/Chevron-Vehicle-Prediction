DBT_PROJECT_YML = """\
name: 'chevron_vehicle_prediction'
version: '1.0.0'
config-version: 2

profile: 'chevron_vehicle_prediction'

model-paths: ["models"]
target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  chevron_vehicle_prediction:
    staging:
      +materialized: view
    marts:
      +materialized: table
"""

PROFILES_YML = """\
chevron_vehicle_prediction:
  target: dev
  outputs:
    dev:
      type: postgres
      host: "{{ env_var('DB_HOST') }}"
      user: "{{ env_var('DB_USER') }}"
      password: "{{ env_var('DB_PASSWORD') }}"
      port: "{{ env_var('DB_PORT') | as_number }}"
      dbname: "{{ env_var('DB_NAME') }}"
      schema: public
      threads: 4
"""

SOURCES_YML = """\
version: 2

sources:
  - name: raw
    schema: public
    tables:
      - name: raw_ev_population
      - name: raw_vehicle_sales
      - name: raw_fuel_economy
      - name: chevron_table
"""

STG_EV_POPULATION_SQL = """\
select 
    vin_1_10,
    county,
    city, 
    state,
    postal_code,
    model_year,
    make,
    model,
    electric_vehicle_type,
    clean_alternative_fuel_vehicle_cafv_eligibility,
    electric_range,
    base_msrp,
    legislative_district,
    dol_vehicle_id,
    vehicle_location,
    electric_utility,
    "col_2020_census_tract"

from {{ source('raw', 'raw_ev_population') }}

"""

STG_CHEVRON_SQL = """\ 
  SELECT
      date, 
      vehicle_category, 
      gvwr_class,
      fuel_type,
      model_year, 
      fuel_technology,
      electric_mile_range,
      number_of_vehicles_registered_at_the_same_address,
      region,
      vehicle_population
    
from {{ source('raw', 'chevron_table') }}

"""

STG_FUEL_ECONOMY_SQL = """ \
SELECT
      vehicle_id,
      year, 
      make, 
      model,
      class,
      drive,
      transmission,
      transmission_type,
      engine_index,
      engine_descriptor,
      engine_cylinders,
      engine_displacement,
      turbocharger,
      supercharger,
      fuel_type,
      fuel_type_1,
      fuel_type_2,
      city_mpg_ft1,
      unrounded_city_mpg_ft1,
      city_mpg_ft2,
      unrounded_city_mpg_ft2,
      city_gasoline_consumption_cd,
      city_electricity_consumption,
      city_utility_factor,
      highway_mpg_ft1,
      unrounded_highway_mpg_ft1,
      highway_mpg_ft2,
      unrounded_highway_mpg_ft2,
      highway_gasoline_consumption_cd,
      highway_electricity_consumption,
      highway_utility_factor,
      unadjusted_city_mpg_ft1,
      unadjusted_highway_mpg_ft1,
      unadjusted_city_mpg_ft2,
      combined_mpg_ft1,
      unrounded_combined_mpg_ft1,
      combined_mpg_ft2,
      unrounded_combined_mpg_ft2,
      combined_electricity_consumption,
      combined_gasoline_consumption_cd,
      combined_utility_factor,
      annual_fuel_cost_ft1,
      annual_fuel_cost_ft2,
      gas_guzzler_tax,
      save_or_spend_5_year,
      annual_consumption_in_barrels_ft1,
      annual_consumption_in_barrels_ft2,
      tailpipe_co2_ft1,
      tailpipe_co2_in_grams_mile_ft1,
      tailpipe_co2_ft2,
      tailpipe_co2_in_grams_mile_ft2,
      fuel_economy_score,
      ghg_score,
      ghg_score_alt_fuel,
      my_mpg_data,
      x2d_passenger_volume,
      x2d_luggage_volume,
      x4d_passenger_volume,
      x4d_luggage_volume,
      hatchback_passenger_volume,
      hatchback_luggage_volume,
      start_stop_technology,
      alternative_fuel_technology,
      electric_motor,
      manufacturer_code,
      gasoline_electricity_blended_cd,
      vehicle_charger,
      alternate_charger,
      hours_to_charge_120v,
      hours_to_charge_240v,
      hours_to_charge_ac_240v,
      composite_city_mpg,
      composite_highway_mpg,
      composite_combined_mpg,
      range_ft1,
      city_range_ft1,
      highway_range_ft1,
      range_ft2,
      city_range_ft2,
      highway_range_ft2
      
FROM {{source('raw', 'raw_fuel_economy')}}
"""

STG_VEHICLE_SALES_SQL = """\
  SELECT
        year,
        make,
        model,
        trim,
        body,
        transmission,
        vin,
        state,
        condition,
        odometer,
        color,
        interior,
        seller,
        mmr,
        sellingprice,
        saledate
        
from {{ source('raw', 'raw_vehicle_sales') }}
"""