# scripts/dbt/setup_dbt_project.py
import shutil
from datetime import datetime
from pathlib import Path

from logs.logger import ErrorCategory, ETL_Logger
from .sql_commands import stage_sql_commands
from .sql_commands import mart_sql_commands


class DBT_Project:
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.root = Path(project_dir)
        self.log = ETL_Logger(ErrorCategory.DBT)
        self.staging_backup_path = None  # set by _backup_staging, used by rollback_staging

    def _write_if_missing(self, path: Path, content: str):
        if path.exists():
            self.log.info(f"Skipping, path already exists: {path}")
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        self.log.info(f"Created: {path}")

    def helper_dbt(self, dbt_args: dict, stage: str):
        if stage not in ("stage", "mart", "test"):
            self.log.error(f"{stage} not found.")
            return
        for group_name, group_files in dbt_args.items():
            for path, content in group_files:
                self.log.info(f"Setting up DBT {stage} ({group_name}): {path}")
                self._write_if_missing(path, content)

    def _backup_staging(self, base_stage_path: Path) -> Path | None:
        """Snapshot the existing staging folder before it gets (re)written."""
        if not base_stage_path.exists() or not any(base_stage_path.iterdir()):
            self.log.info(f"No existing staging content at {base_stage_path}, skipping backup.")
            self.staging_backup_path = None
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_root = self.root / "backups" / "staging"
        backup_root.mkdir(parents=True, exist_ok=True)
        backup_path = backup_root / f"staging_{timestamp}"

        shutil.copytree(base_stage_path, backup_path)
        self.log.info(f"Backed up staging folder to {backup_path}")

        self.staging_backup_path = backup_path
        return backup_path

    def rollback_staging(self) -> bool:
        """Restore the staging folder from the most recent backup taken this run."""
        base_stage_path = self.root / "models" / "staging"

        if self.staging_backup_path is None or not self.staging_backup_path.exists():
            self.log.error("No staging backup available to roll back to.")
            return False

        if base_stage_path.exists():
            shutil.rmtree(base_stage_path)
        shutil.copytree(self.staging_backup_path, base_stage_path)
        self.log.info(f"Rolled back staging folder from {self.staging_backup_path}")
        return True

    def staging_dbt_project(self):
        base_stage_path = self.root / "models" / "staging"

        # snapshot whatever's already there before we touch it
        self._backup_staging(base_stage_path)

        base_stage_path.mkdir(parents=True, exist_ok=True)
        self.log.info(f"Running DBT staging setup in {base_stage_path}")

        dbt_args = {
            "dbt_config": [
                (self.root / "dbt_project.yml", stage_sql_commands.DBT_PROJECT_YML),
                (self.root / "profiles.yml", stage_sql_commands.PROFILES_YML),
                (base_stage_path / "sources.yml", stage_sql_commands.SOURCES_YML),
            ],
            "staging_models": [
                (base_stage_path / "stg_ev_population.sql", stage_sql_commands.STG_EV_POPULATION_SQL),
                (base_stage_path / "stg_chevron_table.sql", stage_sql_commands.STG_CHEVRON_SQL),
                (base_stage_path / "stg_fuel_consumption.sql", stage_sql_commands.STG_FUEL_ECONOMY_SQL),
                (base_stage_path / "stg_vehicle_sales.sql", stage_sql_commands.STG_VEHICLE_SALES_SQL),
            ],
        }
        self.helper_dbt(dbt_args, stage="stage")

    def mart_dbt_setup(self):
        base_mart_path = self.root / "models" / "marts"
        base_mart_path.mkdir(parents=True, exist_ok=True)
        self.log.info(f"Running DBT mart setup in {base_mart_path}")

        mart_args = {
            "config": [
                (base_mart_path / "dbt_mart_project.yml", mart_sql_commands.MART_PROJECT_YAML),
            ],
            "mart": [
                (base_mart_path / "mart_ev_population.sql", mart_sql_commands.MART_BASE_SQL),
            ],
        }
        self.helper_dbt(mart_args, stage="mart")

    def test_cases_dbt(self):
        base_test_path = self.root / "tests" / "generic"
        base_test_path.mkdir(parents=True, exist_ok=True)
        self.log.info(f"Running DBT test setup in {base_test_path}")

        dbt_args = {
            "test_cases": [
                (base_test_path / "test_value_range.sql", mart_sql_commands.TEST_VALUE_RANGE_SQL),
            ],
        }
        self.helper_dbt(dbt_args, stage="test")

    def dbt_main(self):
        self.staging_dbt_project()
        self.mart_dbt_setup()
        self.test_cases_dbt()
        