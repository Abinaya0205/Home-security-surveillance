# cloud/aws_s3.py
import boto3
from botocore.exceptions import ClientError
from config import AWS_CONFIG

class AWSS3Storage:
    """Real AWS S3 storage — needs AWS credentials in config.py"""

    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_CONFIG["access_key"],
            aws_secret_access_key=AWS_CONFIG["secret_key"],
            region_name=AWS_CONFIG["region"]
        )
        self.bucket = AWS_CONFIG["bucket_name"]
        self._ensure_bucket()

    def _ensure_bucket(self):
        try:
            self.s3.head_bucket(Bucket=self.bucket)
            print(f"[OK] S3 bucket '{self.bucket}' exists.")
        except ClientError:
            self.s3.create_bucket(
                Bucket=self.bucket,
                CreateBucketConfiguration={"LocationConstraint": AWS_CONFIG["region"]}
            )
            print(f"[OK] S3 bucket '{self.bucket}' created.")

    def upload(self, local_path: str, remote_name: str = None) -> str:
        if remote_name is None:
            import os
            remote_name = os.path.basename(local_path)
        self.s3.upload_file(local_path, self.bucket, remote_name)
        return f"s3://{self.bucket}/{remote_name}"

    def download(self, remote_name: str, local_path: str) -> str:
        self.s3.download_file(self.bucket, remote_name, local_path)
        return local_path

    def exists(self, remote_name: str) -> bool:
        try:
            self.s3.head_object(Bucket=self.bucket, Key=remote_name)
            return True
        except ClientError:
            return False

    def delete(self, remote_name: str):
        self.s3.delete_object(Bucket=self.bucket, Key=remote_name)