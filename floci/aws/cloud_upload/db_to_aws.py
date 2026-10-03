## What do we need this file to do?
"""
*Check and create s3 buckets if found continue
*check env variables
* compress into parquet file
* upload to s3 
"""
import os, boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv

class aws_cloud:
    def __init__(self):
        load_dotenv()
        self.AWS_ENDPOINT_URL=os.environ.get("AWS_ENDPOINT_URL")
        self.AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.DEFAULT_REGION=os.environ.get("AWS_DEFAULT_REGION")
        self.AWS_BUCKET_NAME=os.environ.get("AWS_BUCKET_NAME")
        
        self.s3_client = boto3.client('s3', 
                                      region_name=self.DEFAULT_REGION, 
                                      config=Config(s3={"addressing_style": "path"})
                                      )

    def check_bucket(self):
        try:
            
            self.s3_client.head_bucket(Bucket=self.AWS_BUCKET_NAME)
            print("Bucket Exists")
        except ClientError as e:
            error_code = str(e.response['Error']['Code'])
            if error_code == "403":
                print("Private Bucket. You dont have the necessary access to view the bucket")
            elif error_code == "404":
                print("Bucket not found")
                print("Creating bucket for you")
                self.bucket_creation()
                
    def bucket_creation(self):
            print("Creating Bucket...")
            kwargs= {"Bucket": self.AWS_BUCKET_NAME}
            if self.DEFAULT_REGION != 'us-east-1':
                kwargs['CreateBucketConfiguration'] = {'LocationConstraint': self.DEFAULT_REGION}
                
            self.s3_client.create_bucket(**kwargs)
            print("Bucket Created")
    def aws_script(self):
        self.check_bucket()





