from dbt.cli.main import dbtRunner, dbtRunnerResult
from scripts.dbt.setup_dbt_project import setup_dbt_project
from logs.logger import ETL_Logger, ErrorCategory
from pathlib import Path

def run_dbt_build(project_dir: str, profile_dir:str):
    
    setup_dbt_project(project_dir)
    log = ETL_Logger(ErrorCategory.DBT)
    dbt = dbtRunner()
    dir_path = Path(project_dir)
    
    dir_path.mkdir(parents=True, exist_ok=True)
    
    log.info(f"Created Directory at {project_dir}")
    
    cli_args = ["build",
                "--project-dir", project_dir,
                "--profiles-dir", profile_dir
                ]
    
    res: dbtRunnerResult = dbt.invoke(cli_args)

    return res