import base64
import os
from io import BytesIO

import boto3
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

bucket_name = os.getenv("bucket_name")
access_key_id = os.getenv("access_key_id")
secret_access_key = os.getenv("secret_access_key")


def list_files_in_bucket():
    # Create an S3 client with access key ID and secret access key
    s3 = boto3.client(
        "s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )

    # List objects within the bucket
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)  # , Prefix="student_face/"

        if "Contents" in response:
            for obj in response["Contents"]:
                print(obj["Key"])
        else:
            print("No objects found in the bucket.")

    except Exception as e:
        print(f"Error listing objects in bucket: {e}")


def delete_files_in_bucket():
    # Create an S3 client with access key ID and secret access key
    s3 = boto3.client(
        "s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )

    # List objects within the bucket
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)

        if "Contents" in response:
            for obj in response["Contents"]:
                # Delete each object
                s3.delete_object(Bucket=bucket_name, Key=obj["Key"])
                print(f"Deleted: {obj['Key']}")
        else:
            print("No objects found in the bucket.")

    except Exception as e:
        print(f"Error deleting objects in bucket: {e}")


def create_folder_in_bucket(folder_name):
    # Create an S3 client with access key ID and secret access key
    s3 = boto3.client(
        "s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )

    # Create an empty object to represent the folder
    folder_key = folder_name + "/"

    try:
        s3.put_object(Bucket=bucket_name, Key=folder_key)
        print(f"Created folder: {folder_name}")

    except Exception as e:
        print(f"Error creating folder: {e}")


def upload_image_from_base64(image_path, base64_image):
    # Create an S3 client with access key ID and secret access key
    s3 = boto3.client(
        "s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )

    # Decode base64 image data
    image_data = base64.b64decode(base64_image)

    # Create a PIL Image from the decoded data
    image = Image.open(BytesIO(image_data))

    # Save the image to a local temporary PNG file
    local_image_path = "myimage.png"
    image.save(local_image_path, format="PNG")

    try:
        # Upload the PNG image file to S3
        s3.upload_file(local_image_path, bucket_name, image_path)
        print(f"Uploaded image to {image_path}")

    except Exception as e:
        print(f"Error uploading image: {e}")


def upload_PDF(PDF_file):
    # Create an S3 client with access key ID and secret access key
    s3 = boto3.client(
        "s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )

    try:
        # Upload the PNG image file to S3
        s3.upload_file(
            f"uploads/{PDF_file}", bucket_name, f"student_document/{PDF_file}"
        )
        print(f"Uploaded image to {PDF_file}")

    except Exception as e:
        print(f"Error uploading image: {e}")


# import base64

# import boto3
# from PIL import Image


def get_image_from_s3(image_key):
    # Create an S3 client with access key ID and secret access key
    s3 = boto3.client(
        "s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )

    try:
        # Download the image file from S3
        response = s3.get_object(Bucket=bucket_name, Key=image_key)
        image_data = response["Body"].read()

        # Create a PIL Image from the image data
        image = Image.open(BytesIO(image_data))

        return image

    except Exception as e:
        print(f"Error getting image: {e}")
        return None


def save_image_as_base64(image):
    try:
        # Convert the image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return base64_image

    except Exception as e:
        print(f"Error saving base64 image: {e}")


def get_image_and_conver_to_base64(image):
    image = get_image_from_s3(image)

    if image is not None:
        # Save the image as base64
        # image_name = image.split("/")[-1].split(".")[0]  # Extract image name from key
        image = save_image_as_base64(image)
        return image
    else:
        print("Image not found or could not be retrieved.")


def get_pdf_from_s3(FilePath):

    # Local file path to save the PDF
    local_file_path = "uploads/downloaded_pdf.pdf"

    s3 = boto3.client(
        "s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )

    try:
        # Download the PDF file from S3 bucket
        s3.download_file(bucket_name, FilePath, local_file_path)
        print(f"PDF file downloaded successfully: {local_file_path}")
    except Exception as e:
        print(f"Error downloading PDF file: {e}")


# list_files_in_bucket()

# delete_files_in_bucket(bucket_name, access_key_id, secret_access_key)


# create_folder_in_bucket(
#     bucket_name, "student_document", access_key_id, secret_access_key
# )

# list_files_in_bucket()
