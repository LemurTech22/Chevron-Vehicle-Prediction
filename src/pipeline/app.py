from pipeline.first_time_setup import database_migrations
from scripts.db import export_db


def run_etl():
    
    database_migrations.database_setup()
