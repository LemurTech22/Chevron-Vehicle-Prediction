from dbt.cli.main import dbtRunner, dbtRunnerResult
from scripts.dbt.setup_dbt_project import DBT_Project
from logs.logger import ETL_Logger, ErrorCategory
from pathlib import Path


def run_dbt_build(project_dir: str, profile_dir: str):
    log = ETL_Logger(ErrorCategory.DBT)

    dir_path = Path(project_dir)
    dir_path.mkdir(parents=True, exist_ok=True)
    if dir_path.exists():
        log.info(f"{dir_path} already exists.")

    dbt_project = DBT_Project(project_dir)
    dbt_project.dbt_main()

    dbt = dbtRunner()
    cli_args = [
        "build",
        "--project-dir", project_dir,
        "--profiles-dir", profile_dir,
    ]
    res: dbtRunnerResult = dbt.invoke(cli_args)

    if not res.success:
        log.error("dbt build failed, rolling back staging to last known-good snapshot.")
        dbt_project.rollback_staging()

    return res