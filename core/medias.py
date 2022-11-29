import boto3
from settings import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME
from fastapi import Path, UploadFile, File
from fastapi.responses import FileResponse

async def upload_file_to_s3(media: UploadFile = File(...)) -> bool:
    s3 = boto3.client("s3", 
    aws_access_key_id=AWS_ACCESS_KEY_ID, 
    region_name=AWS_REGION, 
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    with open(media.file) as bytestream:
        s3.upload_file(
            bytestream,
            S3_BUCKET_NAME,
            media.filename
            #ExtraArgs={'ContentType': 'image/jpg'}
        )
        response = s3.head_object(Bucket=S3_BUCKET_NAME, Key=media.filename)

    return response['ResponseMetadata']['HTTPStatusCode'] == 200 