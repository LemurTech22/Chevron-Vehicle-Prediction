import subprocess
import os
from datetime import datetime
from dotenv import load_dotenv

from logs.logger import ETL_Logger, ErrorCategory
load_dotenv()

class database_export:
    def __init__(self, label: str):
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_PORT = os.getenv("DB_PORT")
        self.OUTPUT_DIR = os.getenv("OUTPUT_DIR")
        self.label = label
        self.log = ETL_Logger(ErrorCategory.DATABASE)         
    def _pg_env(self):
        """Build an environment dict that includes PGPASSWORD, without losing the rest of the shell's env."""
        env = os.environ.copy()
        env["PGPASSWORD"] = self.DB_PASSWORD
        return env

    def export_dbs(self, tables=None):
        # Folder is derived directly from the stage label, so they can never
        # drift out of sync -- e.g. db/dumps/staging_1/, db/dumps/final/
        dump_path = os.path.join(self.OUTPUT_DIR, self.label)
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
        self.log.info(f"Dumping {self.label} tables to {out_path}")
        subprocess.run(cmd, check=True, env=self._pg_env())
        self.log.info(f"Data dumps complete, refer to {out_path}")        

    def db_export_script(self):
        tables = ["raw_ev_population", "raw_vehicle_sales", "raw_fuel_economy", "chevron_table"]

        if self.label == "staging_1":
            self.log.info(f"Creating database dump for {self.label}/Extraction.")        
            self.export_dbs(tables=tables)

        elif self.label == "staging_2":
            self.log.info(f"Creating database dump for {self.label}/Transformation.")        
            self.export_dbs(tables=tables)

        elif self.label == "final":
            self.log.info(f"Creating database dump for {self.label}/Load.")        
            self.export_dbs(tables=["dim_state", "dim_vehicle", "fact_vehicle_sales", "fact_vehicle_population"])

        else:
            self.log.error("f \
                Unknown export stage label: {self.label}. \
                Expected one of: staging_1, staging_2, final \
                Refer to export_db.py")
            raise ValueError(
                f"Unknown export stage label: '{self.label}'.\
                Refer to {self.log.category} logs for more information"
            )