# scripts/dbt/setup_dbt_project.py
from pathlib import Path

from logs.logger import ErrorCategory, ETL_Logger
from .sql_commands import stage_sql_commands
from .sql_commands import mart_sql_commands

def _write_if_missing(path: Path, content: str):
    log = ETL_Logger(ErrorCategory.DBT)
    if path.exists():
        log.info("Skipping path already exists: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    log.info(f"Created: {path}")

def setup_dbt_project(project_dir: str):

    root = Path(project_dir)
    base_stage_path = root / "models" / "staging"
    base_mart_path = root / "models" / "marts"
    base_test_path = root / "tests" / "generic"
    
    _write_if_missing(root / "dbt_project.yml", stage_sql_commands.DBT_PROJECT_YML)
    _write_if_missing(root / "profiles.yml", stage_sql_commands.PROFILES_YML)
    _write_if_missing(base_stage_path / "sources.yml", stage_sql_commands.SOURCES_YML)
    _write_if_missing(base_stage_path / "stg_ev_population.sql", stage_sql_commands.STG_EV_POPULATION_SQL)
    _write_if_missing(base_stage_path / "stg_chevron_table.sql", stage_sql_commands.STG_CHEVRON_SQL)
    _write_if_missing(base_stage_path / "stg_fuel_consumption.sql", stage_sql_commands.STG_FUEL_ECONOMY_SQL)
    _write_if_missing(base_stage_path / "stg_vehicle_sales.sql", stage_sql_commands.STG_VEHICLE_SALES_SQL)    
    (base_mart_path).mkdir(parents=True, exist_ok=True)
    
    _write_if_missing(base_mart_path / "dbt_mart_project.yml", mart_sql_commands.MART_PROJECT_YAML)
    _write_if_missing(base_mart_path / "mart_ev_population.sql", mart_sql_commands.MART_BASE_SQL)
    
    base_test_path.mkdir(parents=True, exist_ok=True)
    _write_if_missing(base_test_path / "test_value_range.sql", mart_sql_commands.TEST_VALUE_RANGE_SQL)
"""    _write_if_missing(base_mart_path / "")
    _write_if_missing(base_mart_path / "")
    _write_if_missing(base_mart_path / "")
    _write_if_missing(base_mart_path / "")
    _write_if_missing(base_mart_path / "")
    _write_if_missing(base_mart_path / "")
"""

