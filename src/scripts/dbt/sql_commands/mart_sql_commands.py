MART_PROJECT_YAML = """
version: 2

models:
  - name: mart_ev_population
    columns:
      - name: make
        tests:
          - accepted_values:
              arguments:
                values: ['KIA', 'FORD', 'PORSCHE', 'TESLA', 'CHEVROLET']
      - name: msrp
        tests:
          - value_range:
              arguments:
                min_value: 20000
                max_value: 300000
      - name: vehicle_model_year
        tests:
          - value_range:
              arguments:
                min_value: 2010
                max_value: 2026

  - name: mart_chevron_population
    columns:
      - name: date
        tests:
          - not_null

      - name: vehicle_category
        tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['P','BS','BT','MC','MH','B','T1','T2','T3','T4','T5','T6','T7']
      - name: gvwr_class
        tests:
          - accepted_values:
              arguments:
                values: [0,1,2,3,4,5,6,7,8]
      - name: fuel_type
        tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['Hydrogen','Natural Gas','Diesel','Gasoline','Electric']
      - name: vehicle_model_year
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 2010
                max_value: 2026
      - name: fuel_technology
        tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['FCEV','PHEV','BEV','ICE']
      - name: number_of_vehicles_registered_at_the_same_address
        tests:
          - accepted_values:
              arguments:
                values: [1,2,3]
      - name: region
        tests:
          - accepted_values:
              arguments:
                values: ['Statewide']
      - name: vehicle_population
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1
                max_value: 100000

  - name: fuel_economy
    columns:
      - name: vehicle_id
        tests:
          - unique
          - not_null

      - name: year
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 2010
                max_value: 2026

      - name: make
        tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['S and S Coach Company  E.p. Dutton', 'Ford', 'Maserati', 'Dodge', 'Excalibur Autos', 'Infiniti', 'J.K. Motors', 'Fisker', 'TVR Engineering Ltd', 'Grumman Allied Industries', 'Dacia', 'CODA Automotive', 'PAS Inc - GMC', 'SRT', 'ASC Incorporated', 'Audi', 'Mcevoy Motors', 'Import Trade Services', 'Lexus', 'Import Foreign Auto Sales Inc', 'Isis Imports Ltd', 'General Motors', 'Jeep', 'American Motors Corporation', 'Vector', 'Cadillac', 'Sterling', 'Autokraft Limited', 'Texas Coach Company', 'Panther Car Company Limited', 'Evans Automobiles', 'Ferrari', 'GMC', 'Maybach', 'Lincoln', 'Honda', 'Spyker', 'Chevrolet', 'JBA Motorcars, Inc.', 'Quantum Technologies', 'Daihatsu', 'Environmental Rsch and Devp Corp', 'Porsche', 'Pininfarina', 'Rolls-Royce', 'Tesla', 'Jaguar', 'Renault', 'Kia', 'Saleen Performance', 'CX Automotive', 'Pagani', 'Bugatti', 'Ruf Automobile Gmbh', 'McLaren Automotive', 'Fiat', 'Buick', 'Merkur', 'CCC Engineering', 'Mercury', 'Wallace Environmental', 'Roush Performance', 'Toyota', 'Bertone', 'Grumman Olson', 'Mahindra', 'Avanti Motor Corporation', 'VPG', 'BMW Alpina', 'PAS, Inc', 'Federal Coach', 'MINI', 'Bentley', 'Peugeot', 'Pontiac', 'Plymouth', 'Lambda Control Systems', 'Volvo', 'Panoz Auto-Development', 'Acura', 'Suzuki', 'Bitter Gmbh and Co. Kg', 'Aston Martin', 'BYD', 'Mitsubishi', 'AM General', 'E. P. Dutton, Inc.', 'Qvale', 'Chrysler', 'London Taxi', 'Mobility Ventures LLC', 'Isuzu', 'Ram', 'Daewoo', 'Morgan', 'Panos', 'Scion', 'Shelby', 'Saturn', 'Bill Dovell Motor Car Company', 'Vixen Motor Company', 'Alfa Romeo', 'smart', 'Lotus', 'Lamborghini', 'Mercedes-Benz', 'Oldsmobile', 'Superior Coaches Div E.p. Dutton', 'Goldacre', 'Consulier Industries Inc', 'Land Rover', 'Nissan', 'Kenyon Corporation Of America', 'Genesis', 'Aurora Cars Ltd', 'Saab', 'Hyundai', 'Yugo', 'London Coach Co Inc', 'Saleen', 'Geo', 'Subaru', 'Laforza Automobile Inc', 'Tecstar, LP', 'Mazda', 'Red Shift Ltd.', 'BMW', 'Volkswagen', 'Eagle', 'Azure Dynamics', 'Hummer', 'Dabryan Coach Builders Inc', 'Volga Associated Automobile']
      - name: model
        tests:
          - not_null
      - name: class
        tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['Sport Utility Vehicle - 4WD', 'Special Purpose Vehicles/4wd', 'Special Purpose Vehicle 4WD', 'Large Cars', 'Vans Passenger', 'Special Purpose Vehicle', 'Standard Sport Utility Vehicle 4WD', 'Minivan - 4WD', 'Special Purpose Vehicles', 'Minicompact Cars', 'Midsize Station Wagons', 'Compact Cars', 'Special Purpose Vehicles/2wd', 'Midsize Cars', 'Sport Utility Vehicle - 2WD', 'Standard Pickup Trucks', 'Standard Pickup Trucks 2WD', 'Standard Pickup Trucks 4WD', 'Small Sport Utility Vehicle 2WD', 'Vans, Cargo Type', 'Small Sport Utility Vehicle 4WD', 'Small Pickup Trucks', 'Small Station Wagons', 'Midsize-Large Station Wagons', 'Vans, Passenger Type', 'Two Seaters', 'Minivan - 2WD', 'Special Purpose Vehicle 2WD', 'Standard Pickup Trucks/2wd', 'Small Pickup Trucks 4WD', 'Small Pickup Trucks 2WD', 'Standard Sport Utility Vehicle 2WD', 'Subcompact Cars', 'Vans']
      - name: drive
        tests:
          - accepted_values:
              arguments:
                values: ['Part-Time 4-Wheel Drive','4 Wheel or All-Wheel Drive','Rear-Wheel Drive','N/A','All-Wheel Drive',' Front-Wheel Drive','4-Wheel Drive','2-Wheel Drive']
      - name: transmission
      - name: transmission_type
      - name: engine_index
      - name: engine_descriptor
      - name: engine_cylinders
      - name: engine_displacement
      - name: turbocharger
      - name: supercharger
      - name: fuel_type
        tests:
          - accepted_values:
              arguments:
                values: ['Gasoline or propane','Premium and Electricity','Premium Gas or Electricity','Regular','CNG','Electricity','Gasoline or natural gas','Diesel','Regular Gas and Electricity','Gasoline or E85', 'Midgrade', 'Premium', 'Regular Gas or Electricity', 'Premium or E85']
      - name: fuel_type_1
        tests:
          - accepted_values:
              arguments:
                values: ['Natural Gas', 'Diesel', 'Midgrade Gasoline','Electricity','Premium Gasoline','Regular Gasoline']
      - name: fuel_type_2
      - name: city_mpg_ft1
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1
                max_value: 98
      - name: unrounded_city_mpg_ft1
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1
                max_value: 98

      - name: city_mpg_ft2
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1
                max_value: 98
      - name: unrounded_city_mpg_ft2
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1
                max_value: 98
      - name: city_gasoline_consumption_cd
      - name: city_electricity_consumption
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1
                max_value: 98
      - name: city_utility_factor
      - name: highway_mpg_ft1
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1
                max_value: 98
      - name: unrounded_highway_mpg_ft1
      - name: highway_mpg_ft2
      - name: unrounded_highway_mpg_ft2
      - name: highway_gasoline_consumption_cd
      - name: highway_electricity_consumption
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1
                max_value: 98
      - name: highway_utility_factor
      - name: unadjusted_city_mpg_ft1
      - name: unadjusted_highway_mpg_ft1
      - name: unadjusted_city_mpg_ft2
      - name: combined_mpg_ft1
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 6
                max_value: 98
      - name: unrounded_combined_mpg_ft1
      - name: combined_mpg_ft2
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 6
                max_value: 98
      - name: unrounded_combined_mpg_ft2
      - name: combined_electricity_consumption
      - name: combined_gasoline_consumption_cd
      - name: combined_utility_factor
      - name: annual_fuel_cost_ft1
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 100
                max_value: 8000
      - name: annual_fuel_cost_ft2
      - name: gas_guzzler_tax
      - name: save_or_spend_5_year
      - name: annual_consumption_in_barrels_ft1
      - name: annual_consumption_in_barrels_ft2
      - name: tailpipe_co2_ft1
      - name: tailpipe_co2_in_grams_mile_ft1
      - name: tailpipe_co2_ft2
      - name: tailpipe_co2_in_grams_mile_ft2
      - name: fuel_economy_score
      - name: ghg_score
      - name: ghg_score_alt_fuel
      - name: my_mpg_data
      - name: x2d_passenger_volume
      - name: x2d_luggage_volume
      - name: x4d_passenger_volume
      - name: x4d_luggage_volume
      - name: hatchback_passenger_volume
      - name: hatchback_luggage_volume
      - name: start_stop_technology
      - name: alternative_fuel_technology
      - name: electric_motor
      - name: manufacturer_code
      - name: gasoline_electricity_blended_cd
      - name: vehicle_charger
      - name: alternate_charger
      - name: hours_to_charge_120v
      - name: hours_to_charge_240v
      - name: hours_to_charge_ac_240v
      - name: composite_city_mpg
      - name: composite_highway_mpg
      - name: composite_combined_mpg
      - name: range_ft1
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 0
                max_value: 350
      - name: city_range_ft1
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 0
                max_value: 300
      - name: highway_range_ft1
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 0
                max_value: 400
      - name: range_ft2
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 0
                max_value: 350
      - name: city_range_ft2
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 0
                max_value: 300
      - name: highway_range_ft2
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 0
                max_value: 400
"""


EV_MART_BASE_SQL = """\
with base as (
    SELECT 
      CAST(model_year AS INT) as vehicle_model_year,
      make, 
      CAST(NULLIF(REPLACE(electric_range::text, ',', ''), '') as INT) as electric_range,
      CAST(NULLIF(REPLACE(base_msrp::text, ',', ''), '') as INT) as msrp 
    FROM {{ ref('stg_ev_population') }}   
)

SELECT *
FROM base
WHERE electric_range > 100
  AND msrp > 20000 AND msrp < 300000
  AND vehicle_model_year >= 2010
  AND make IS NOT NULL
"""


CHEVRON_MART_BASE_SQL = """\
with base as (
    SELECT 
      date,
      region,
      CAST(model_year AS INT) as vehicle_model_year,
      number_of_vehicles_registered_at_the_same_address,
      COALESCE(NULLIF(REPLACE(gvwr_class::text, ',', ''), '')::INT, 0) AS gvwr_class,
      NULLIF(REPLACE(fuel_type::text, 'NULL', ''), '') AS fuel_type,
      NULLIF(REPLACE(vehicle_category::text, 'NULL', ''), '') AS vehicle_category,
      NULLIF(REPLACE(fuel_technology::text, 'NULL', ''), '') AS fuel_technology,
      CAST(NULLIF(REPLACE(vehicle_population::text, 'NULL', ''), '') AS INT) AS vehicle_population
    FROM {{ ref('stg_chevron_table') }}
)

SELECT *
FROM base
WHERE vehicle_model_year >= 2010 
  AND vehicle_population > 1
  AND fuel_type IS NOT NULL
  AND vehicle_category IS NOT NULL;
"""

MART_VEHICLE_FUEL_CONSUMPTION= """
with base as (
  SELECT 
    *, 
    CAST(NULLIF(REPLACE(year::text, ',', ''), '') AS INT) AS model_year,
    CAST(NULLIF(REPLACE(year::text, ',', ''), '') AS INT) AS average_range 
  FROM {{ref('stg_fuel_consumption')}}
  )
  
SELECT * 
FROM base  
WHERE 
  model_year >= 2010 
AND 
  average_range > 0;
"""



TEST_VALUE_RANGE_SQL = """\
{% test value_range(model, column_name, min_value, max_value) %}

select *
from {{ model }}
where {{ column_name }} < {{ min_value }}
   or {{ column_name }} > {{ max_value }}

{% endtest %}
"""