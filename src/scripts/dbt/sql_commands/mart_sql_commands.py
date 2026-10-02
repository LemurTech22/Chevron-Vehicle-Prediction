MART_PROJECT_YAML = """
version: 2

models:
  - name: mart_ev_population
    columns:
      - name: make
        data_tests:
          - accepted_values:
              arguments:
                values: ['KIA', 'FORD', 'PORSCHE', 'TESLA', 'CHEVROLET']
      - name: msrp
        data_tests:
          - value_range:
              arguments:
                min_value: 20000
                max_value: 300000
      - name: vehicle_model_year
        data_tests:
          - value_range:
              arguments:
                min_value: 2000
                max_value: 2026

  - name: mart_vehicle_population
    columns:
      - name: date
        data_tests:
          - not_null
      - name: vehicle_category
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['P','BS','BT','MC','MH','B','T1','T2','T3','T4','T5','T6','T7']
      - name: gvwr_class
        data_tests:
          - accepted_values:
              arguments:
                values: [0,1,2,3,4,5,6,7,8]
      - name: fuel_type
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['Hydrogen','Natural Gas','Diesel','Gasoline','Electric']
      - name: vehicle_model_year
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 2000
                max_value: 2026
      - name: fuel_technology
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['FCEV','PHEV','BEV','ICE']
      - name: number_of_vehicles_registered_at_the_same_address
        data_tests:
          - accepted_values:
              arguments:
                values: [0,1,2,3]
              config:
                severity: warn
      - name: region
        data_tests:
          - accepted_values:
              arguments:
                values: ['Statewide']
      - name: vehicle_population
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1

  - name: mart_vehicle_fuel_consumption
    columns:
      - name: vehicle_id
        data_tests:
          - unique
          - not_null
      - name: model_year
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1984
                max_value: 2026
      - name: make
        data_tests:
          - not_null
      - name: model
        data_tests:
          - not_null
      - name: city_mpg
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1
                max_value: 150
      - name: highway_mpg
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1
                max_value: 150
      - name: combined_mpg
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1
                max_value: 150
      - name: annual_fuel_cost
        data_tests:
          - value_range:
              arguments:
                min_value: 100
                max_value: 50000

  - name: mart_vehicle_sales
    columns:
      - name: model_year
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 2010
                max_value: 2026
      - name: make
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['Acura', 'Airstream', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Buick',
                'Cadillac', 'Chevrolet', 'Chrysler', 'Daewoo', 'Dodge', 'Ferrari', 'FIAT', 'Fisker', 'Ford',
                'Geo', 'GMC', 'Honda', 'HUMMER', 'Hyundai', 'Infiniti', 'Isuzu', 'Jaguar', 'Jeep', 'Kia',
                'Lamborghini', 'Land Rover', 'Lexus', 'Lincoln', 'Lotus', 'Maserati', 'Mazda', 'Mercedes-Benz', 'Mercury', 'MINI', 'Mitsubishi',
                'Nissan', 'Oldsmobile', 'Plymouth', 'Pontiac', 'Porsche', 'Ram', 'Rolls-Royce', 'Saab', 'Saturn', 'Scion', 'smart', 'Subaru', 'Suzuki',
                'Tesla', 'Toyota', 'Volkswagen', 'Volvo'
                ]
      - name: model
        data_tests:
          - not_null
      - name: sellingprice
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 0
                max_value: 200000

  - name: mart_VEHICLE_INFORMATION
    columns:
      - name: model_year
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1982
                max_value: 2026
      - name: make
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['Acura', 'Airstream', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler',
                'Daewoo', 'Dodge', 'Ferrari', 'FIAT', 'Fisker', 'Ford', 'Geo', 'GMC', 'Honda', 'HUMMER', 'Hyundai', 'Infiniti', 'Isuzu',
                'Jaguar', 'Jeep', 'Kia', 'Lamborghini', 'Land Rover', 'Lexus', 'Lincoln', 'Lotus', 'Maserati', 'Mazda', 'Mercedes-Benz',
                'Mercury', 'MINI', 'Mitsubishi', 'Nissan', 'Oldsmobile', 'Plymouth', 'Pontiac', 'Porsche', 'Ram', 'Rolls-Royce', 'Saab',
                'Saturn', 'Scion', 'smart', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo']
              config:
                severity: warn
      - name: model
        data_tests:
          - not_null
      - name: class
      - name: fuel_type
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['gas', 'diesel']
      - name: city_mpg
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 6
                max_value: 60
      - name: highway_mpg
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 6
                max_value: 65
      - name: combined_mpg
        data_tests:
          - not_null
      - name: annual_fuel_cost
        data_tests:
          - value_range:
              arguments:
                min_value: 500
                max_value: 6500
      - name: sold_count
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 0

  - name: mart_EV_INFORMATION
    columns:
      - name: model_year
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1998
                max_value: 2026
      - name: make
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['Audi', 'BMW', 'Chevrolet', 'Fiat', 'Ford', 'Genesis', 'Honda',
                         'Hyundai', 'Jaguar', 'Kia', 'Lexus', 'Lucid', 'Mazda',
                         'Mercedes-Benz', 'MINI', 'Mitsubishi', 'Nissan', 'Polestar',
                         'Porsche', 'Rivian', 'smart', 'Subaru', 'Tesla', 'Toyota',
                         'Volkswagen', 'Volvo']
              config:
                severity: warn
      - name: model
        data_tests:
          - not_null
      - name: class
      - name: fuel_type_1
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['Electricity']
      - name: city_mpg
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 20
                max_value: 180
      - name: highway_mpg
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 20
                max_value: 160
      - name: total_range
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 30
                max_value: 600
      - name: annual_fuel_cost
        data_tests:
          - value_range:
              arguments:
                min_value: 200
                max_value: 4000
      - name: registered_count
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 0
      - name: avg_electric_range
        data_tests:
          - value_range:
              arguments:
                min_value: 0
                max_value: 600

  - name: mart_VEHICLE_WEIGHT_CLASS
    columns:
      - name: model_year
        data_tests:
          - not_null
      - name: vehicle_category
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['P','BS','BT','MC','MH','B','T1','T2','T3','T4','T5','T6','T7']
      - name: vehicle_type
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['passenger','motorcycle','truck','motor_home','bus']
      - name: duty_category
        data_tests:
          - accepted_values:
              arguments:
                values: ['light_duty','medium_duty','heavy_duty','varies']
      - name: fuel_type
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['gas','diesel','hydrogen','natural_gas','electric']
      - name: fuel_technology
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['FCEV','PHEV','BEV','ICE']
      - name: vehicle_population
        data_tests:
          - not_null
          - value_range:
              arguments:
                min_value: 1
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
  AND vehicle_category IS NOT NULL
"""

MART_VEHICLE_FUEL_CONSUMPTION = """\
with base as (
  SELECT
    *,
    CAST(NULLIF(REPLACE(year::text, ',', ''), '') AS INT) AS model_year,
    CAST(NULLIF(REPLACE(range_ft1::text, ',', ''), '') AS INT) AS vehicle_range,
    CAST(NULLIF(city_mpg_ft1::text, '') AS NUMERIC)          AS city_mpg,
    CAST(NULLIF(highway_mpg_ft1::text, '') AS NUMERIC)       AS highway_mpg,
    CAST(NULLIF(combined_mpg_ft1::text, '') AS NUMERIC)      AS combined_mpg,
    CAST(NULLIF(annual_fuel_cost_ft1::text, '') AS NUMERIC)  AS annual_fuel_cost,

    CASE
      WHEN supercharger IS NULL THEN false
      WHEN lower(trim(supercharger::text)) IN ('na', 'n/a', '') THEN false
      ELSE true
    END AS has_supercharger,

    CASE
      WHEN turbocharger IS NULL THEN false
      WHEN lower(trim(turbocharger::text)) IN ('na', 'n/a', '') THEN false
      ELSE true
    END AS has_turbocharger

  FROM {{ ref('stg_fuel_consumption') }}
)

SELECT *
FROM base
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
    AND make IS NOT NULL
    AND model_year >= 2010
    AND model IS NOT NULL
    AND sellingprice >= 1000
    AND sellingprice <= 200000
"""

VEHICLE_INFORMATION_SQL = """\
with sales_agg as (
    select
        lower(trim(make))  as make_key,
        lower(trim(model)) as model_key,
        model_year,
        count(*) as sold_count
    from {{ ref('mart_vehicle_sales') }}
    group by 1, 2, 3
)

select
    cast(nullif(replace(f.year::text, ',', ''), '') as int) as model_year,
    f.make,
    f.model,
    f.class,
    case
        when lower(trim(f.fuel_type_1::text)) like '%gasoline%' then 'gas'
        when lower(trim(f.fuel_type_1::text)) like '%diesel%'   then 'diesel'
    end as fuel_type,
    cast(nullif(f.city_mpg_ft1, '') as numeric)          as city_mpg,
    cast(nullif(f.highway_mpg_ft1, '') as numeric)       as highway_mpg,
    cast(nullif(f.combined_mpg_ft1, '') as numeric)      as combined_mpg,
    cast(nullif(f.annual_fuel_cost_ft1, '') as numeric)  as annual_fuel_cost,
    coalesce(s.sold_count, 0) as sold_count
from {{ ref('stg_fuel_consumption') }} as f
left join sales_agg as s
    on lower(trim(f.make))  = s.make_key
   and lower(trim(f.model)) = s.model_key
   and cast(nullif(replace(f.year::text, ',', ''), '') as int) = s.model_year
where lower(trim(f.fuel_type_1)) like '%gasoline%'
   or lower(trim(f.fuel_type_1)) like '%diesel%'
"""

VEHICLE_EV_INFORMATION_SQL = """\
with ev_agg as (
    select
        lower(trim(make))  as make_key,
        lower(trim(model)) as model_key,
        count(*) as registered_count,
        avg(nullif(nullif(electric_range::text, ''), '0')::numeric) as avg_electric_range
    from {{ ref('stg_ev_population') }}
    group by 1, 2
),

fuel as (
    select
        cast(nullif(replace(year::text, ',', ''), '') as int) as model_year,
        make,
        model,
        class,
        fuel_type_1,
        cast(nullif(city_mpg_ft1, '') as numeric)          as city_mpg,
        cast(nullif(highway_mpg_ft1, '') as numeric)       as highway_mpg,
        cast(nullif(range_ft1, '') as numeric)             as total_range,
        cast(nullif(annual_fuel_cost_ft1, '') as numeric)  as annual_fuel_cost
    from {{ ref('stg_fuel_consumption') }}
    where lower(trim(fuel_type_1)) like '%electric%'
)

select
    f.model_year,
    f.make,
    f.model,
    f.class,
    f.fuel_type_1,
    f.city_mpg,
    f.highway_mpg,
    f.total_range,
    f.annual_fuel_cost,
    coalesce(e.registered_count, 0) as registered_count,
    e.avg_electric_range
from fuel as f
left join ev_agg as e
    on lower(trim(f.make))  = e.make_key
   and lower(trim(f.model)) = e.model_key
where f.total_range >= 30
  and f.total_range <= 600
"""

VEHICLE_WEIGHT_CLASS_MART_SQL = """\
with base as (
    select
        vehicle_model_year as model_year,
        vehicle_category,
        fuel_type,
        fuel_technology,
        vehicle_population
    from {{ ref('mart_vehicle_population') }}
)

select
    model_year,
    vehicle_category,
    case
        when upper(trim(vehicle_category)) = 'P'  then 'passenger'
        when upper(trim(vehicle_category)) = 'MC' then 'motorcycle'
        when upper(trim(vehicle_category)) in ('T1','T2','T3','T4','T5','T6','T7') then 'truck'
        when upper(trim(vehicle_category)) = 'MH' then 'motor_home'
        when upper(trim(vehicle_category)) in ('B','BS','BT') then 'bus'
    end as vehicle_type,
    -- T1-T7 mapping is provisional until confirmed against the data dictionary
    case
        when upper(trim(vehicle_category)) in ('P','MC','T1','T2') then 'light_duty'
        when upper(trim(vehicle_category)) in ('T3','T4','T5','T6') then 'medium_duty'
        when upper(trim(vehicle_category)) = 'T7' then 'heavy_duty'
        when upper(trim(vehicle_category)) in ('B','BS','BT','MH') then 'varies'
    end as duty_category,
    case lower(trim(fuel_type))
        when 'hydrogen'    then 'hydrogen'
        when 'natural gas' then 'natural_gas'
        when 'diesel'      then 'diesel'
        when 'gasoline'    then 'gas'
        when 'electric'    then 'electric'
    end as fuel_type,
    fuel_technology,
    vehicle_population
from base
"""

TEST_VALUE_RANGE_SQL = """\
{% test value_range(model, column_name, min_value=none, max_value=none) %}

{% set conditions = [] %}
{% if min_value is not none %}
    {% do conditions.append(column_name ~ ' < ' ~ min_value) %}
{% endif %}
{% if max_value is not none %}
    {% do conditions.append(column_name ~ ' > ' ~ max_value) %}
{% endif %}

select *
from {{ model }}
where {{ conditions | join(' or ') if conditions else '1 = 0' }}

{% endtest %}
"""