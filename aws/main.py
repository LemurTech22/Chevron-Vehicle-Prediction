from aws.cloud_upload.db_to_aws import aws_cloud
from aws.glue.glue_worker import glue

def run_aws_script(local_dir: str, s3_prefix: str):
    aws_cloud().aws_script(local_dir, s3_prefix)
    glue().run_glue_worker(parquet_root=local_dir, s3_prefix=s3_prefix)
    