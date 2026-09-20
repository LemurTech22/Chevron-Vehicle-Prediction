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
              min_value: 20000
              max_value: 300000
      - name: model_year
        tests:
          - value_range:
              min_value: 2010
              max_value: 2026
"""


MART_BASE_SQL = """\
with base as (
    SELECT CAST(REPLACE(model_year::text, ',', '') as INT) as model_year,
    make, 
    CAST(NULLIF(REPLACE(electric_range::text, ',', ''), '') as INT) as electric_range,
    CAST(NULLIF(REPLACE(base_msrp::text, ',' ,''), '') as INT) as msrp 
FROM {{ref('stg_ev_population')}}   
)

SELECT *
FROM base   
WHERE electric_range > 100 AND msrp > 10000 AND msrp < 200000 AND model_year > 2010
"""

TEST_VALUE_RANGE_SQL = """\
{% test value_range(model, column_name, min_value, max_value) %}

select *
from {{ model }}
where {{ column_name }} < {{ min_value }}
   or {{ column_name }} > {{ max_value }}

{% endtest %}
"""