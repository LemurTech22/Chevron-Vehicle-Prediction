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
          - not_null
      - name: model_year
        tests:
          - not_null
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
WHERE electric_range > 100 AND msrp > 10000 AND msrp < 200000
"""
