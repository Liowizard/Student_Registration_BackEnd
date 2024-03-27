import base64
from io import BytesIO

import boto3
from PIL import Image


def list_files_in_bucket():
    # Create an S3 client with access key ID and secret access key
    s3 = boto3.client(
        "s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )

    # List objects within the bucket
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)

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


def upload_image_from_base64(folder_name, base64_image, image_name):
    # Create an S3 client with access key ID and secret access key
    s3 = boto3.client(
        "s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )

    # Decode base64 image data
    image_data = base64.b64decode(base64_image)

    # Create a PIL Image from the decoded data
    image = Image.open(BytesIO(image_data))

    # Save the image to a local temporary PNG file
    local_image_path = f"/tmp/{image_name}.png"
    image.save(local_image_path, format="PNG")

    # Construct the full key (object path) for the image in the folder
    image_key = folder_name + "/" + image_name + ".png"

    try:
        # Upload the PNG image file to S3
        s3.upload_file(local_image_path, bucket_name, image_key)
        print(f"Uploaded image to {image_key}")

    except Exception as e:
        print(f"Error uploading image: {e}")


# list_files_in_bucket(bucket_name, access_key_id, secret_access_key)

# delete_files_in_bucket(bucket_name, access_key_id, secret_access_key)


# create_folder_in_bucket(
#     bucket_name, "student_document", access_key_id, secret_access_key
# )

list_files_in_bucket()
