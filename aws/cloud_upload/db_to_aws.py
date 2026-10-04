"""

 compress into parquet file
 upload to s3 
! add logging
"""
import os, boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from pathlib import Path
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
            
    def db_upload_to_s3(self,local_dir: str,s3_prefix:str = ""):
        try:
            local_path = Path(local_dir)
            if not local_path.exists():
                print("error export dir not found")
            else:
                print(f"{local_path} found: proceeding")
                uploaded=0
                for file_path in local_path.rglob("*"):
                    if file_path.is_file():
                        relative_path = file_path.relative_to(local_path)
                        s3_key = "/".join(
                            filter(None, [s3_prefix, str(relative_path).replace(os.sep, "/")]))
                        
                        self.s3_client.upload_file(str(file_path), self.AWS_BUCKET_NAME,s3_key)
                        print(f"{file_path} uploaded to {self.AWS_BUCKET_NAME}")
                        uploaded +=1
            return uploaded
        except Exception as e:
            raise ValueError 
    def aws_script(self,local_dir: str, s3_prefix: str = ""):
        self.check_bucket()
        return self.db_upload_to_s3(local_dir=local_dir,s3_prefix=s3_prefix)
