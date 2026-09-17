# scripts/dbt/setup_dbt_project.py
from pathlib import Path

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
    vin_(1-10),
    county,
    city, 
    state,
    postal_code,
    model_year,
    make,
    model,
    electric_vehicle_type,
    clean_alternative_fuel_vehicle_(cafv)_eligibility,
    electric_range,
    base_msrp,
    legislative_district,
    dol_vehicle_id,
    vehicle_location,
    electric_utility,
    "2020_census_tract"

from {{ source('raw', 'raw_ev_population') }}
"""


def _write_if_missing(path: Path, content: str):
    if path.exists():
        print(f"Skipping (already exists): {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"Created: {path}")


def setup_dbt_project(project_dir: str):
    """
    Idempotently scaffold a dbt project at `project_dir`.
    Safe to call every run -- existing files are never overwritten,
    only missing ones are created. This lets a fresh clone or a
    Docker container get a working dbt project with zero manual setup,
    while a developer's own edits to models are never clobbered.
    """
    root = Path(project_dir)
    _write_if_missing(root / "dbt_project.yml", DBT_PROJECT_YML)
    _write_if_missing(root / "profiles.yml", PROFILES_YML)
    _write_if_missing(root / "models" / "staging" / "sources.yml", SOURCES_YML)
    _write_if_missing(root / "models" / "staging" / "stg_ev_population.sql", STG_EV_POPULATION_SQL)
    (root / "models" / "marts").mkdir(parents=True, exist_ok=True)