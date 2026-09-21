from dbt.cli.main import dbtRunner, dbtRunnerResult
from scripts.dbt.setup_dbt_project import DBT_Project
from logs.logger import ETL_Logger, ErrorCategory
from pathlib import Path

def run_dbt_build(project_dir: str, profile_dir:str):
    dbt_project = DBT_Project(project_dir)
    dbt_project.dbt_main()
    
    log = ETL_Logger(ErrorCategory.DBT)
    dbt = dbtRunner()
    dir_path = Path(project_dir)
    
    dir_path.mkdir(parents=True, exist_ok=True) 
    log.info(f"Creating Directory at {project_dir}")
    if dir_path.exists:
        log.info(f"{dir_path} already exists.")
    
    cli_args = ["build",
                "--project-dir", project_dir,
                "--profiles-dir", profile_dir
                ]
    res: dbtRunnerResult = dbt.invoke(cli_args)
    return res
