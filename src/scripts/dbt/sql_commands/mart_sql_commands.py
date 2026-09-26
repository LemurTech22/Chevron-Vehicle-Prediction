MART_PROJECT_YAML = """
version: 2

models:
  - name: mart_ev_population
    columns:
      - name: make
        tests:
          - accepted_values:
              values: ['KIA', 'FORD', 'PORSCHE', 'TESLA', 'CHEVROLET']
      - name: msrp
        tests:
          - value_range:
              min_value: 20000
              max_value: 300000
      - name: vehicle_model_year
        tests:
          - value_range:
              min_value: 2010
              max_value: 2026

  - name: mart_chevron_population
    columns:
      - name: date
      - name: vehicle_category
        tests:
          - accepted_values:
              values: ['P','BS','BT','MC','MH','B','T1','T2','T3','T4','T5','T6','T7']
      - name: gvwr_class
        tests:
          - accepted_values:
              values: [0,1,2,3,4,5,6,7,8]
      - name: fuel_type
        tests:
          - accepted_values:
              values: ['Hydrogen','Natural Gas','Diesel','Gasoline','Electric']
      - name: vehicle_model_year
        tests:
          - value_range:
              min_value: 2010
              max_value: 2026
      - name: fuel_technology
        tests:
          - accepted_values:
              values: ['FCEV','PHEV','BEV','ICE']
      - name: number_of_vehicles_registered_at_the_same_address
        tests:
          - accepted_values:
              values: [1,2,3]
      - name: region
        tests:
          - accepted_values:
              values: ['Statewide']
      - name: vehicle_population
        tests:
          - value_range:
              min_value: 1
              max_value: 100000
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


TEST_VALUE_RANGE_SQL = """\
{% test value_range(model, column_name, min_value, max_value) %}

select *
from {{ model }}
where {{ column_name }} < {{ min_value }}
   or {{ column_name }} > {{ max_value }}

{% endtest %}
"""