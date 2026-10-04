import os
import boto3
import pyarrow.parquet as pq
from botocore.config import Config
from dotenv import load_dotenv


# Parquet logical type (str(pyarrow type)) -> Glue/Hive column type.
# Falls back to "string" for anything unmapped -- safe default, since Athena
# can still read it, just without native typed filtering on that column.
GLUE_TYPE_MAP = {
    "int32": "int",
    "int64": "bigint",
    "float": "float",
    "double": "double",
    "string": "string",
    "large_string": "string",
    "bool": "boolean",
    "timestamp[us]": "timestamp",
    "timestamp[ns]": "timestamp",
    "timestamp[s]": "timestamp",
    "date32[day]": "date",
}


def glue_columns_from_parquet(parquet_file_path: str) -> list:
    """Read a Parquet file's embedded schema and translate it to Glue
    column definitions, so we never have to guess or hand-maintain a schema.
    """
    schema = pq.read_schema(parquet_file_path)
    columns = []
    for field in schema:
        glue_type = GLUE_TYPE_MAP.get(str(field.type), "string")
        columns.append({"Name": field.name, "Type": glue_type})
    return columns


class glue:
    def __init__(self):
        load_dotenv()

        self.session = boto3.session.Session(
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_DEFAULT_REGION"),
        )

        self.bucket = os.environ.get("AWS_BUCKET_NAME")
        self.db_name = os.environ.get("GLUE_DATABASE_NAME", "chevron_warehouse")

        self.glue_client = self.session.client(
            "glue",
            endpoint_url=os.environ.get("AWS_ENDPOINT_URL"),
            config=Config(s3={"addressing_style": "path"}),
        )

    def glue_database(self):
        try:
            self.glue_client.get_database(Name=self.db_name)
            print(f"Glue database {self.db_name} already exists.")
        except self.glue_client.exceptions.EntityNotFoundException:
            self.glue_client.create_database(DatabaseInput={"Name": self.db_name})
            print(f"Created Glue database '{self.db_name}'.")

    def register_table(self, table_name: str, s3_location: str, sample_parquet_file: str):
        """Create (or replace) a Glue table pointing at s3_location, with its
        schema read directly from sample_parquet_file. No crawler involved --
        Parquet already carries its own schema, so there's nothing to infer.
        """
        columns = glue_columns_from_parquet(sample_parquet_file)

        table_input = {
            "Name": table_name,
            "StorageDescriptor": {
                "Location": s3_location,
                "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
                "OutputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
                "SerdeInfo": {
                    "SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
                },
                "Columns": columns,
            },
            "TableType": "EXTERNAL_TABLE",
        }

        try:
            self.glue_client.get_table(DatabaseName=self.db_name, Name=table_name)
            self.glue_client.update_table(DatabaseName=self.db_name, TableInput=table_input)
            print(f"Updated Glue table '{table_name}' -> {s3_location}")
        except self.glue_client.exceptions.EntityNotFoundException:
            self.glue_client.create_table(DatabaseName=self.db_name, TableInput=table_input)
            print(f"Created Glue table '{table_name}' -> {s3_location}")

    def run_glue_worker(self, parquet_root: str, s3_prefix: str):
        """Walk parquet_root (export_db.py's output) two levels deep --
        layer, then table -- and register one Glue table per table folder.
        Matches the actual layout export_tables_to_parquet() produces:

            {parquet_root}/<layer>/<table_name>/<table_name>.parquet

        and the matching S3 layout aws_cloud.py uploads to:

            s3://{bucket}/{s3_prefix}/<layer>/<table_name>/<table_name>.parquet
        """
        self.glue_database()

        if not os.path.isdir(parquet_root):
            print(f"Parquet root not found: {parquet_root} -- nothing to register.")
            return

        for layer_name in sorted(os.listdir(parquet_root)):
            layer_dir = os.path.join(parquet_root, layer_name)
            if not os.path.isdir(layer_dir):
                continue

            for table_name in sorted(os.listdir(layer_dir)):
                table_dir = os.path.join(layer_dir, table_name)
                if not os.path.isdir(table_dir):
                    continue

                parquet_files = [f for f in os.listdir(table_dir) if f.endswith(".parquet")]
                if not parquet_files:
                    print(f"No .parquet file found in {table_dir} -- skipping.")
                    continue

                sample_file = os.path.join(table_dir, parquet_files[0])
                s3_location = f"s3://{self.bucket}/{s3_prefix}/{layer_name}/{table_name}/"

                self.register_table(table_name=table_name, s3_location=s3_location, sample_parquet_file=sample_file)