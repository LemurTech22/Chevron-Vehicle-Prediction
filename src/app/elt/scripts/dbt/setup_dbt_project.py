# scripts/dbt/setup_dbt_project.py
from pathlib import Path

from logs.logger import ErrorCategory, ETL_Logger
from . import sql_commands

def _write_if_missing(path: Path, content: str):
    log = ETL_Logger(ErrorCategory.DBT)
    if path.exists():
        log.info("Skipping path already exists: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    log.info(f"Created: {path}")

def setup_dbt_project(project_dir: str):
    """
    Idempotently scaffold a dbt project at `project_dir`.
    Safe to call every run -- existing files are never overwritten,
    only missing ones are created. This lets a fresh clone or a
    Docker container get a working dbt project with zero manual setup,
    while a developer's own edits to models are never clobbered.
    """
    root = Path(project_dir)
    _write_if_missing(root / "dbt_project.yml", sql_commands.DBT_PROJECT_YML)
    _write_if_missing(root / "profiles.yml", sql_commands.PROFILES_YML)
    _write_if_missing(root / "models" / "staging" / "sources.yml", sql_commands.SOURCES_YML)
    _write_if_missing(root / "models" / "staging" / "stg_ev_population.sql", sql_commands.STG_EV_POPULATION_SQL)
    _write_if_missing(root / "models" / "staging" / "stg_chevron_table.sql", sql_commands.STG_CHEVRON_SQL)
    _write_if_missing(root / "models" / "staging" / "stg_fuel_consumption.sql", sql_commands.STG_FUEL_ECONOMY_SQL)
    _write_if_missing(root / "models" / "staging" / "stg_vehicle_sales.sql", sql_commands.STG_VEHICLE_SALES_SQL)    
    (root / "models" / "marts").mkdir(parents=True, exist_ok=True)
    