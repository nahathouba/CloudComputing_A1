import boto3
import json
import os
import requests
from botocore.exceptions import ClientError
from AWS_Creds import *

BUCKET_NAME = 's3733745-artist-images'
A1_JSON_PATH = 'a1.json'
IMAGE_TEMP_DIR = './temp'

s3Client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=region_name
)


def createArtistImageBucket():
    try:
        s3Client.head_bucket(Bucket=BUCKET_NAME)
        print(f"Bucket {BUCKET_NAME} already exists.")
    except Exception as e:
        if 'Not Found' in str(e):
            s3Client.create_bucket(Bucket=BUCKET_NAME)
            print(f"Bucket {BUCKET_NAME} created.")
        else:
            print(f"Error checking bucket {BUCKET_NAME}: {e}")


def downloadArtistImage():
    with open(A1_JSON_PATH) as file:
        imageData = json.load(file)

    for img in imageData['songs']:
        imgURL = img['img_url']
        imgName = img['artist']
        response = requests.get(imgURL)
        if response.status_code == 200:
            if not os.path.exists(IMAGE_TEMP_DIR):
                os.makedirs(IMAGE_TEMP_DIR)
            # Get the file extension from the URL
            fileExtension = os.path.splitext(imgURL)[1]

            # Create the local file path by joining the IMAGE_TEMP_DIR and the image name with extension
            localFilePath = os.path.join(
                IMAGE_TEMP_DIR, imgName + fileExtension)

            with open(localFilePath, 'wb') as f:
                f.write(response.content)
                f.close()
                print(f"Image Downloaded: {imgName}")


def uploadArtistImageS3():
    if not os.path.exists(IMAGE_TEMP_DIR):
        print(f"Local Directory {IMAGE_TEMP_DIR} does not exist")
        return

    for img in os.listdir(IMAGE_TEMP_DIR):
        localFilePath = os.path.join(IMAGE_TEMP_DIR, img)
        s3Client.upload_file(localFilePath, BUCKET_NAME,
                             img, ExtraArgs={'ACL': 'public-read'})
        print(f"Image Uploaded: {img}")
        os.remove(localFilePath)


def bucketExists():
    try:
        s3Client.head_bucket(Bucket=BUCKET_NAME)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise
