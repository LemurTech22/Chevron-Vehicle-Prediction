from pipeline.first_time_setup import database_migrations
from scripts.db import export_db


def run_etl():
    
    database_migrations.setup()
    export_db.database_export("staging_1")
