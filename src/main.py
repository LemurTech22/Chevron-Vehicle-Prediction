from pipeline.app import run_etl
from floci.aws.cloud_upload.db_to_aws import aws_cloud
if __name__ == "__main__":
    run_etl()
    aws_cloud().aws_script()
