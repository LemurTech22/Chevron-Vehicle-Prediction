from first_time_setup import database_migrations
from scripts.db import export_db


def run_etl():
    
    database_migrations.setup()
    database_export = export_db.database_export("staging_1")
