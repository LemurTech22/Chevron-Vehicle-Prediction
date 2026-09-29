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
                min_value: 2000
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
                min_value: 2000
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
                min_value: 2000
                max_value: 2026

      - name: make
        tests:
          - not_null
          - accepted_values:
              arguments:
                values: [
                  'S and S Coach Company  E.p. Dutton', 'Ford', 'Maserati', 'Dodge', 'Excalibur Autos', 'Infiniti', 'J.K. Motors', 'Fisker', 'TVR Engineering Ltd', 'Grumman Allied Industries', 'Dacia', 'CODA Automotive', 
                  'PAS Inc - GMC', 'SRT', 'ASC Incorporated', 'Audi', 'Mcevoy Motors', 'Import Trade Services', 'Lexus', 'Import Foreign Auto Sales Inc', 'Isis Imports Ltd', 'General Motors', 'Jeep', 'American Motors Corporation', 
                  'Vector', 'Cadillac', 'Sterling', 'Autokraft Limited', 'Texas Coach Company', 'Panther Car Company Limited', 'Evans Automobiles', 'Ferrari', 'GMC', 'Maybach', 'Lincoln', 'Honda', 'Spyker', 'Chevrolet', 'JBA Motorcars, Inc.', 
                  'Quantum Technologies', 'Daihatsu', 'Environmental Rsch and Devp Corp', 'Porsche', 'Pininfarina', 'Rolls-Royce', 'Tesla', 'Jaguar', 'Renault', 'Kia', 'Saleen Performance', 'CX Automotive', 'Pagani', 'Bugatti', 'Ruf Automobile Gmbh', 
                  'McLaren Automotive', 'Fiat', 'Buick', 'Merkur', 'CCC Engineering', 'Mercury', 'Wallace Environmental', 'Roush Performance', 'Toyota', 'Bertone', 'Grumman Olson', 'Mahindra', 'Avanti Motor Corporation', 'VPG', 'BMW Alpina', 'PAS, Inc', 
                  'Federal Coach', 'MINI', 'Bentley', 'Peugeot', 'Pontiac', 'Plymouth', 'Lambda Control Systems', 'Volvo', 'Panoz Auto-Development', 'Acura', 'Suzuki', 'Bitter Gmbh and Co. Kg', 'Aston Martin', 'BYD', 'Mitsubishi', 'AM General', 'E. P. Dutton, Inc.', 
                  'Qvale', 'Chrysler', 'London Taxi', 'Mobility Ventures LLC', 'Isuzu', 'Ram', 'Daewoo', 'Morgan', 'Panos', 'Scion', 'Shelby', 'Saturn', 'Bill Dovell Motor Car Company', 'Vixen Motor Company', 'Alfa Romeo', 'smart', 'Lotus', 'Lamborghini', 'Mercedes-Benz', 
                  'Oldsmobile', 'Superior Coaches Div E.p. Dutton', 'Goldacre', 'Consulier Industries Inc', 'Land Rover', 'Nissan', 'Kenyon Corporation Of America', 'Genesis', 'Aurora Cars Ltd', 'Saab', 'Hyundai', 'Yugo', 'London Coach Co Inc', 'Saleen', 'Geo', 'Subaru', 
                  'Laforza Automobile Inc', 'Tecstar, LP', 'Mazda', 'Red Shift Ltd.', 'BMW', 'Volkswagen', 'Eagle', 'Azure Dynamics', 'Hummer', 'Dabryan Coach Builders Inc', 'Volga Associated Automobile'
                  ]
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
          - value_range:
              arguments:
                min_value: 1
                max_value: 98

      - name: city_mpg_ft2
        tests:
          - value_range:
              arguments:
                min_value: 1
                max_value: 98
      - name: unrounded_city_mpg_ft2
        tests:
          - value_range:
              arguments:
                min_value: 1
                max_value: 150
      - name: city_gasoline_consumption_cd
      - name: city_electricity_consumption
        tests:
          - value_range:
              arguments:
                min_value: 0
                max_value: 150
      - name: city_utility_factor
      - name: highway_mpg_ft1
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1
                max_value: 150
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
                max_value: 150
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
                max_value: 150
      - name: unrounded_combined_mpg_ft1
      - name: combined_mpg_ft2
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 6
                max_value: 150
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
                max_value: 50000
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

  - name: mart_vehicle_sales
    columns:
      - name: model_year
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
                values: ['Acura', 'Airstream', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Daewoo', 'Dodge', 'Ferrari', 'FIAT', 'Fisker', 'Ford', 'Geo', 'GMC', 'Honda', 'HUMMER', 'Hyundai', 'Infiniti', 'Isuzu', 'Jaguar', 'Jeep', 'Kia', 'Lamborghini', 'Land Rover', 'Lexus', 'Lincoln', 'Lotus', 'Maserati', 'Mazda', 'Mercedes-Benz', 'Mercury', 'MINI', 'Mitsubishi', 'Nissan', 'Oldsmobile', 'Plymouth', 'Pontiac', 'Porsche', 'Ram', 'Rolls-Royce', 'Saab', 'Saturn', 'Scion', 'smart', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo']
      - name: model
        tests:
          - not_null
      - name: trim
      - name: body
      - name: transmission
      - name: vin
      - name: state
      - name: condition
      - name: odometer
      - name: color
      - name: interior
      - name: seller
      - name: mmr
      - name: sellingprice
        tests:
          - not_null
          - value_range:
              arguments:
                min_value: 0
                max_value: 200000
      - name: saledate
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
  AND vehicle_model_year >= 2000
  AND make IS NOT NULL
"""


CHEVRON_MART_BASE_SQL = """\
with base as (
    SELECT 
      date,
      region,
      CAST(model_year AS INT) as vehicle_model_year,
      COALESCE(NULLIF(REPLACE(gvwr_class::text, ',', ''), '')::INT, 0) AS gvwr_class,
    CASE
      WHEN number_of_vehicles_registered_at_the_same_address::text LIKE '≥%'
        THEN NULLIF(REPLACE(number_of_vehicles_registered_at_the_same_address::text, '≥', ''), '')::INT
      ELSE COALESCE(NULLIF(REPLACE(number_of_vehicles_registered_at_the_same_address::text, ',', ''), '')::INT, 0)
    END AS number_of_vehicles_registered_at_the_same_address,
      NULLIF(REPLACE(fuel_type::text, 'NULL', ''), '') AS fuel_type,
      NULLIF(REPLACE(vehicle_category::text, 'NULL', ''), '') AS vehicle_category,
      NULLIF(REPLACE(fuel_technology::text, 'NULL', ''), '') AS fuel_technology,
      CAST(NULLIF(REPLACE(vehicle_population::text, 'NULL', ''), '') AS INT) AS vehicle_population
    FROM {{ ref('stg_chevron_table') }}
)

SELECT *
FROM base
WHERE vehicle_model_year >= 2000 
  AND vehicle_population > 1
  AND fuel_type IS NOT NULL
  AND vehicle_category IS NOT NULL;
"""

MART_VEHICLE_FUEL_CONSUMPTION= """
with base as (
  SELECT *,
  CAST(NULLIF(REPLACE(year::text, ',', ''), '') AS INT) AS model_year,
  CAST(NULLIF(REPLACE(range_ft1::text, ',', ''), '') AS INT) AS vehicle_range,

  CASE
    when supercharger is null then false
    when lower(trim(supercharger::text)) in ('na','n/a','') THEN false
    else true
  end as has_supercharger,
  
  CASE
    when turbocharger is null then false
    when lower(trim(supercharger::text)) in ('na','n/a','') THEN false
    else true
  end as has_turbocharger
  
  FROM {{ref('stg_fuel_consumption')}}
  )
  
SELECT * 
FROM base;
"""


MART_VEHICLE_SALES = """\
with base as (
    SELECT
      CAST(NULLIF(REPLACE(year::text, ',', ''), '') AS INT) AS model_year,
      CASE LOWER(TRIM(make))
        WHEN 'acura' THEN 'Acura'
        WHEN 'airstream' THEN 'Airstream'
        WHEN 'aston martin' THEN 'Aston Martin'
        WHEN 'audi' THEN 'Audi'
        WHEN 'bentley' THEN 'Bentley'
        WHEN 'bmw' THEN 'BMW'
        WHEN 'buick' THEN 'Buick'
        WHEN 'cadillac' THEN 'Cadillac'
        WHEN 'chevrolet' THEN 'Chevrolet'
        WHEN 'chev truck' THEN 'Chevrolet'
        WHEN 'chrysler' THEN 'Chrysler'
        WHEN 'daewoo' THEN 'Daewoo'
        WHEN 'dodge' THEN 'Dodge'
        WHEN 'dodge tk' THEN 'Dodge'
        WHEN 'ferrari' THEN 'Ferrari'
        WHEN 'fiat' THEN 'FIAT'
        WHEN 'fisker' THEN 'Fisker'
        WHEN 'ford' THEN 'Ford'
        WHEN 'ford tk' THEN 'Ford'
        WHEN 'ford truck' THEN 'Ford'
        WHEN 'geo' THEN 'Geo'
        WHEN 'gmc' THEN 'GMC'
        WHEN 'gmc truck' THEN 'GMC'
        WHEN 'honda' THEN 'Honda'
        WHEN 'hummer' THEN 'HUMMER'
        WHEN 'hyundai' THEN 'Hyundai'
        WHEN 'hyundai tk' THEN 'Hyundai'
        WHEN 'infiniti' THEN 'Infiniti'
        WHEN 'isuzu' THEN 'Isuzu'
        WHEN 'jaguar' THEN 'Jaguar'
        WHEN 'jeep' THEN 'Jeep'
        WHEN 'kia' THEN 'Kia'
        WHEN 'lamborghini' THEN 'Lamborghini'
        WHEN 'land rover' THEN 'Land Rover'
        WHEN 'landrover' THEN 'Land Rover'
        WHEN 'lexus' THEN 'Lexus'
        WHEN 'lincoln' THEN 'Lincoln'
        WHEN 'lotus' THEN 'Lotus'
        WHEN 'maserati' THEN 'Maserati'
        WHEN 'mazda' THEN 'Mazda'
        WHEN 'mazda tk' THEN 'Mazda'
        WHEN 'mercedes' THEN 'Mercedes-Benz'
        WHEN 'mercedes-b' THEN 'Mercedes-Benz'
        WHEN 'mercedes-benz' THEN 'Mercedes-Benz'
        WHEN 'mercury' THEN 'Mercury'
        WHEN 'mini' THEN 'MINI'
        WHEN 'mitsubishi' THEN 'Mitsubishi'
        WHEN 'nissan' THEN 'Nissan'
        WHEN 'oldsmobile' THEN 'Oldsmobile'
        WHEN 'plymouth' THEN 'Plymouth'
        WHEN 'pontiac' THEN 'Pontiac'
        WHEN 'porsche' THEN 'Porsche'
        WHEN 'ram' THEN 'Ram'
        WHEN 'rolls-royce' THEN 'Rolls-Royce'
        WHEN 'saab' THEN 'Saab'
        WHEN 'saturn' THEN 'Saturn'
        WHEN 'scion' THEN 'Scion'
        WHEN 'smart' THEN 'smart'
        WHEN 'subaru' THEN 'Subaru'
        WHEN 'suzuki' THEN 'Suzuki'
        WHEN 'tesla' THEN 'Tesla'
        WHEN 'toyota' THEN 'Toyota'
        WHEN 'volkswagen' THEN 'Volkswagen'
        WHEN 'vw' THEN 'Volkswagen'
        WHEN 'volvo' THEN 'Volvo'
        ELSE NULL  -- catches junk like 'dot' and any future unrecognized value;
                   -- filtered out below by make IS NOT NULL
      END AS make,
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
      CAST(NULLIF(REPLACE(sellingprice::text, ',', ''), '') AS INT) AS sellingprice,
      saledate
    FROM {{ ref('stg_vehicle_sales') }}
)

SELECT *
FROM base
WHERE
    transmission IS NOT NULL
    AND trim IS NOT NULL
    AND make is NOT NULL
    AND model_year >= 2010
    AND make IS NOT NULL
    AND model IS NOT NULL
    AND sellingprice >= 1000
    AND sellingprice <= 200000
"""


VEHICLE_INFORMATION_SQL = """\
with sales_agg as (
    select
        make,
        model,
        model_year,
        count(model) as sold_count
    from mart_vehicle_sales
    group by make, model, model_year
)

select
    cast(nullif(replace(f.year::text, ',', ''), '') as int) as model_year,
    f.make,
    f.model,
    f.class,
    f.fuel_type_1,
    cast(nullif(f.city_mpg_ft1, '') as numeric) as city_mpg,
    cast(nullif(f.highway_mpg_ft1, '') as numeric) as highway_mpg,
    cast(nullif(f.combined_mpg_ft1, '') as numeric) as total_range,
    cast(nullif(f.annual_fuel_cost_ft1, '') as numeric) as annual_fuel_cost,
    s.sold_count
from stg_fuel_consumption as f
left join sales_agg as s
    on lower(trim(f.make)) = lower(trim(s.make))
    and lower(trim(f.model)) = lower(trim(s.model))
    and cast(nullif(replace(f.year::text, ',', ''), '') as int) = s.model_year
where lower(trim(f.fuel_type_1)) like '%gas%'
   or lower(trim(f.fuel_type_1)) like '%diesel%'
"""

VEHICLE_EV_INFORMATION_SQL = """\
  with ev_agg as (
      select
          make,
          model,
          count(*) as registered_count,
          avg(nullif(electric_range, '')::numeric) as avg_electric_range
      from {{ ref('stg_ev_population') }}
      group by make, model
  )

  select
      cast(nullif(replace(f.year::text, ',', ''), '') as int) as model_year,
      f.make,
      f.model,
      f.class,
      f.fuel_type_1,
      cast(nullif(f.city_mpg_ft1, '') as numeric) as city_mpg,
      cast(nullif(f.highway_mpg_ft1, '') as numeric) as highway_mpg,
      cast(nullif(f.range_ft1, '') as numeric) as total_range,
      cast(nullif(f.annual_fuel_cost_ft1, '') as numeric) as annual_fuel_cost,
      e.registered_count,
      e.avg_electric_range
  from {{ ref('stg_fuel_consumption') }} as f
  left join ev_agg as e
      on lower(trim(f.make)) = lower(trim(e.make))
      and lower(trim(f.model)) = lower(trim(e.model))
  where lower(trim(f.fuel_type_1)) like '%electric%'
"""


TEST_VALUE_RANGE_SQL = """\
{% test value_range(model, column_name, min_value, max_value) %}

select *
from {{ model }}
where {{ column_name }} < {{ min_value }}
   or {{ column_name }} > {{ max_value }}

{% endtest %}
"""


  
  
  