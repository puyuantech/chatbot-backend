import boto3
from bases.globals import settings


class S3Connector:

    @staticmethod
    def get_conn():
        return boto3.resource(
            's3',
            region_name=settings['AWS_REGION_NAME'],
            aws_access_key_id=settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=settings['AWS_SECRET_ACCESS_KEY'],
        )

