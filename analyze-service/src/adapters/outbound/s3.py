from io import BytesIO

import aioboto3
from botocore.config import Config

from src.domain.adapters.outbound.s3 import IS3Client


class S3Client(IS3Client):
    """A client for interacting with an S3-compatible object storage service."""

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint: str,
        region_name: str,
        bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint,
            "region_name": region_name,
            "config": Config(signature_version="s3v4"),
        }
        self.bucket_name = bucket_name
        self.session = aioboto3.Session()

    async def get_file(self, key: str) -> BytesIO:
        async with self.session.client("s3", **self.config) as s3:
            response = await s3.get_object(Bucket=self.bucket_name, Key=key)
            body = await response["Body"].read()
            return BytesIO(body)
