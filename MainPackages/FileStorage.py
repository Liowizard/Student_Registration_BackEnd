import base64
import os
import time
from io import BytesIO

import boto3
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

bucketName = os.getenv("bucketName")
accessKeyId = os.getenv("accessKeyId")
secretAccessKey = os.getenv("secretAccessKey")


def listFilesInBucket():

    # Create an S3 client with access key ID and secret access key
    s3 = boto3.client(
        "s3", aws_access_key_id=accessKeyId, aws_secret_access_key=secretAccessKey
    )

    # List objects within the bucket
    try:
        TotalList = s3.list_objects_v2(Bucket=bucketName)  # , Prefix="student_face/"

        if "Contents" in TotalList:
            for obj in TotalList["Contents"]:
                print(obj["Key"])
        else:
            print("No objects found in the bucket.")

    except Exception as e:
        print(f"Error listing objects in bucket: {e}")


def deleteFilesInBucket():
    # Create an S3 client with access key ID and secret access key
    s3 = boto3.client(
        "s3", aws_access_key_id=accessKeyId, aws_secret_access_key=secretAccessKey
    )

    # List objects within the bucket
    try:
        TotalList = s3.list_objects_v2(Bucket=bucketName)

        if "Contents" in TotalList:
            for obj in TotalList["Contents"]:
                # Delete each object
                s3.delete_object(Bucket=bucketName, Key=obj["Key"])
                print(f"Deleted: {obj['Key']}")
        else:
            print("No objects found in the bucket.")

    except Exception as e:
        print(f"Error deleting objects in bucket: {e}")


def createFolderInBucket(folderName):
    # Create an S3 client with access key ID and secret access key
    s3 = boto3.client(
        "s3", aws_access_key_id=accessKeyId, aws_secret_access_key=secretAccessKey
    )

    # Create an empty object to represent the folder
    folderKey = folderName + "/"

    try:
        s3.put_object(Bucket=bucketName, Key=folderKey)
        print(f"Created folder: {folderName}")

    except Exception as e:
        print(f"Error creating folder: {e}")


def uploadImageFromBase64(imagePath, base64Image):
    # Create an S3 client with access key ID and secret access key
    s3 = boto3.client(
        "s3", aws_access_key_id=accessKeyId, aws_secret_access_key=secretAccessKey
    )

    # Decode base64 image data
    imageData = base64.b64decode(base64Image)

    # Create a PIL Image from the decoded data
    image = Image.open(BytesIO(imageData))

    # Save the image to a local temporary PNG file
    localImagePath = "myimage.png"
    image.save(localImagePath, format="PNG")

    try:
        # Upload the PNG image file to S3
        s3.upload_file(localImagePath, bucketName, imagePath)
        print(f"Uploaded image to {imagePath}")

    except Exception as e:
        print(f"Error uploading image: {e}")


def getImageFromS3(imageKey):
    # Create an S3 client with access key ID and secret access key
    s3 = boto3.client(
        "s3", aws_access_key_id=accessKeyId, aws_secret_access_key=secretAccessKey
    )

    try:
        # Download the image file from S3
        response = s3.get_object(Bucket=bucketName, Key=imageKey)
        imageData = response["Body"].read()

        # Create a PIL Image from the image data
        image = Image.open(BytesIO(imageData))

        return image

    except Exception as e:
        print(f"Error getting image: {e}")
        return None


def saveImageAsBase64(image):
    try:
        # Convert the image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        base64Image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return base64Image

    except Exception as e:
        print(f"Error saving base64 image: {e}")


def getImageAndConverBoBase64(image):
    begin = time.time()
    image = getImageFromS3(image)

    if image is not None:
        # Save the image as base64
        # image_name = image.split("/")[-1].split(".")[0]  # Extract image name from key
        image = saveImageAsBase64(image)
        end = time.time()
        print(f"Total time to take the image from S3 bucket {end - begin}")
        return image
    else:
        print("Image not found or could not be retrieved.")
