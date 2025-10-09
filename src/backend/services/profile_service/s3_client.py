import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class S3Client:
    """AWS S3 client for file uploads"""

    def __init__(self):
        self.bucket_name = os.getenv("S3_BUCKET", "linkedin-networking-storage")
        self.region = os.getenv("AWS_REGION", "us-east-1")

        # Initialize S3 client
        self.s3_client = boto3.client(
            's3',
            region_name=self.region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

    def upload_file(self, file_content: bytes, s3_key: str) -> bool:
        """
        Upload file to S3 bucket

        Args:
            file_content: File content as bytes
            s3_key: S3 object key (path)

        Returns:
            True if upload successful, raises exception otherwise
        """
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ServerSideEncryption='AES256'  # Enable encryption at rest
            )
            return True
        except ClientError as e:
            raise Exception(f"Failed to upload file to S3: {str(e)}")

    def download_file(self, s3_key: str) -> bytes:
        """
        Download file from S3 bucket

        Args:
            s3_key: S3 object key (path)

        Returns:
            File content as bytes
        """
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return response['Body'].read()
        except ClientError as e:
            raise Exception(f"Failed to download file from S3: {str(e)}")

    def delete_file(self, s3_key: str) -> bool:
        """
        Delete file from S3 bucket

        Args:
            s3_key: S3 object key (path)

        Returns:
            True if deletion successful
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return True
        except ClientError as e:
            raise Exception(f"Failed to delete file from S3: {str(e)}")

    def generate_presigned_url(self, s3_key: str, expiration: int = 3600) -> str:
        """
        Generate presigned URL for file access

        Args:
            s3_key: S3 object key (path)
            expiration: URL expiration time in seconds (default: 1 hour)

        Returns:
            Presigned URL
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            raise Exception(f"Failed to generate presigned URL: {str(e)}")

    def file_exists(self, s3_key: str) -> bool:
        """
        Check if file exists in S3 bucket

        Args:
            s3_key: S3 object key (path)

        Returns:
            True if file exists, False otherwise
        """
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return True
        except ClientError:
            return False
