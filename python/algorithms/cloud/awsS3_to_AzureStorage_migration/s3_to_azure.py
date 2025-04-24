import os
import boto3
from azure.storage.blob import BlobServiceClient, ContentSettings
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from .env
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

AZURE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
AZURE_CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME')

LOCAL_DOWNLOAD_DIR = 's3_download_temp'


def download_from_s3():
    print("Downloading files from S3...")
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )

    try:
        os.makedirs(LOCAL_DOWNLOAD_DIR, exist_ok=True)
        objects = s3.list_objects_v2(Bucket=AWS_BUCKET_NAME)

        if 'Contents' in objects:
            for obj in objects['Contents']:
                key = obj['Key']
                local_path = os.path.join(LOCAL_DOWNLOAD_DIR, key)
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                print(f"Downloading {key} to {local_path}")
                s3.download_file(AWS_BUCKET_NAME, key, local_path)
        else:
            print("No files found in the S3 bucket.")
    except NoCredentialsError:
        print("AWS credentials not available. Please check your .env file.")
        exit(1)


def upload_to_azure():
    print("Uploading files to Azure Blob Storage...")
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

    for root, dirs, files in os.walk(LOCAL_DOWNLOAD_DIR):
        for filename in files:
            local_file_path = os.path.join(root, filename)
            blob_name = os.path.relpath(local_file_path, LOCAL_DOWNLOAD_DIR)
            print(f"Uploading {local_file_path} as {blob_name}")

            with open(local_file_path, "rb") as data:
                container_client.upload_blob(
                    name=blob_name,
                    data=data,
                    overwrite=True,
                    content_settings=ContentSettings(content_type="application/octet-stream")
                )


if __name__ == "__main__":
    # Check for required environment variables
    required_env_vars = [
        'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION', 'AWS_BUCKET_NAME',
        'AZURE_STORAGE_CONNECTION_STRING', 'AZURE_CONTAINER_NAME'
    ]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Missing environment variables: {', '.join(missing_vars)}")
        exit(1)

    download_from_s3()
    upload_to_azure()
    print("Migration completed successfully.")
