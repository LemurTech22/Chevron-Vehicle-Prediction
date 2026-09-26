import sys
from pipeline.first_time_setup import database_migrations
from pipeline.first_time_setup.database_migrations import helper_dbt

def run_etl():
    skip = "--skip-dbt" in sys.argv
    if not skip:
        try:
            ans = input("Skip to DBT? ")
            skip = ans.strip().lower() in ("y", "yes")
        except (ValueError, OSError):
            skip = False

    if skip:
        helper_dbt()
    else:
        database_migrations.database_setup()