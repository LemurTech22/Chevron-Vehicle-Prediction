import subprocess
import os
import duckdb
from datetime import datetime
from dotenv import load_dotenv

from logs.logger import ETL_Logger, ErrorCategory
load_dotenv()

class database_export:
    def __init__(self):
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_PORT = os.getenv("DB_PORT")
        self.OUTPUT_DIR = os.getenv("OUTPUT_DIR")
        self.log = ETL_Logger(ErrorCategory.DATABASE)         
    def _pg_env(self):
        """Build an environment dict that includes PGPASSWORD, without losing the rest of the shell's env."""
        env = os.environ.copy()
        env["PGPASSWORD"] = self.DB_PASSWORD
        return env

    def export_dbs(self, tables=None):

        dump_path = os.path.join(self.OUTPUT_DIR)
        os.makedirs(dump_path, exist_ok=True)
        self.log.info(f"Created SQL dump directory at {dump_path}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(dump_path, f"{self.DB_NAME}_{timestamp}.dump")

        cmd = ["pg_dump", "-F", "c",
               "-h", self.DB_HOST, "-U", self.DB_USER, "-d", self.DB_NAME, "-p", self.DB_PORT,
               "-f", out_path]
        if tables:
            for t in tables:
                cmd += ["-t", t]
        self.log.info(f"Dumping tables to {out_path}")
        subprocess.run(cmd, check=True, env=self._pg_env())
        self.log.info(f"Data dumps complete, refer to {out_path}")
        return out_path
    
    def export_table_to_parquet(self, layer: str, tables: list):
        root = os.path.join(self.OUTPUT_DIR, "parquet", layer)
        os.makedirs(root, exist_ok=True)
        con = duckdb.connect()
        con.execute("INSTALL postgres;")
        con.execute("LOAD postgres;")
        con.execute(f"""
            ATTACH 'host={self.DB_HOST} port={self.DB_PORT} dbname={self.DB_NAME}
            user={self.DB_USER} password={self.DB_PASSWORD}'
            AS pg (TYPE postgres, READ_ONLY);
        """)
        try:
            for table in tables:
                table_dir = os.path.join(root, table)
                os.makedirs(table_dir, exist_ok=True)
                out_file = os.path.join(table_dir, f"{table}.parquet")
                self.log.info(f"Exporting {layer}.{table} -> {out_file}")
                con.execute(f"COPY (SELECT * FROM pg.{table}) TO '{out_file}' (FORMAT PARQUET)")
        finally:
            con.execute("DETACH pg;")
            con.close()
        return root

    def db_export_script(self):
        LAYERS = {
            "raw": ["chevron_table", "raw_ev_population", "raw_fuel_economy", "raw_vehicle_sales"],
            "staging": ["stg_chevron_table", "stg_ev_population", "stg_fuel_consumption", "stg_vehicle_sales"],
            "marts": [
                "mart_vehicle_fuel_consumption", "mart_vehicle_weight_class", "mart_ev_information",
                "mart_vehicle_sales", "mart_vehicle_information", "mart_ev_population", "mart_vehicle_population",
            ],
        }
        
        PG_DUMP_LAYERS = ["taw", "marts"]
        parquet_root = os.path.join(self.OUTPUT_DIR, "parquet")
        for layer, tables in LAYERS.items():
            if layer in PG_DUMP_LAYERS:
                self.export_dbs(tables=tables)
            self.log.info(f"Compressing table {tables} into parquet")
            self.export_table_to_parquet(layer=layer, tables=tables)
        self.log.info(f"Creating database dump for Extraction.")        
        return parquet_root