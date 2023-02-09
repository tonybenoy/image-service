import uuid

import boto3

from src.config import Settings
from src.constants import IMAGE_STATUS
from src.db import Image, Session
from src.image import cartoon_image


def get_s3_client():
    """Get S3 client.
    Returns:
        boto3.client: The S3 client."""
    s3_client = boto3.client(
        "s3",
        endpoint_url=Settings.S3_ENDPOINT,
        aws_access_key_id=Settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=Settings.S3_ACCESS_KEY,
        aws_session_token=None,
        verify=False,
    )
    return s3_client


def upload_image_to_s3(image_name: str, image, bucket: str = "test"):
    """Upload image to S3.
    Args:
        image_name (str): The image name.
        image (file): The image file.
        bucket (str, optional): The bucket name. Defaults to "test".
    Returns:
        str: The image key."""
    filename = f"{uuid.uuid4().hex}{image_name}"
    s3_client = get_s3_client()
    s3_client.upload_fileobj(image, bucket, filename)
    return filename


def process_image(img_id: int, bucket: str = "test"):
    """Process image and upload to S3 and update the database.
    Args:
        img_id (int): The image id.
        bucket (str, optional): The bucket name. Defaults to "test".
    Returns:
        None"""
    db = Session()
    image = (
        db.query(Image)
        .filter(Image.id == img_id, Image.processed == IMAGE_STATUS.UNPROCESSED.value)
        .first()
    )
    if not image:
        return
    image_obj = get_image_obj(image.key, bucket)
    image_bytes = image_obj["Body"].read()
    image.processed = IMAGE_STATUS.PROCESSING.value
    db.commit()

    result = cartoon_image(image_bytes)
    try:
        result.seek(0)
    except AttributeError:
        image.processed = IMAGE_STATUS.FAILED.value
        db.commit()
        return
    processed_file = upload_image_to_s3(f"p{image.name}", result, bucket)
    image.processed_key = processed_file
    image.processed = IMAGE_STATUS.PROCESSED.value
    image.processed_key = processed_file
    db.commit()
    db.close()
    return


def get_image_obj(key, bucket):
    """Get image object.
    Args:
         key (str): The image key.
         bucket (str): The bucket name.
      Returns:
         dict: The image object.
    """
    s3_client = get_s3_client()
    return s3_client.get_object(Bucket=bucket, Key=key)


def get_image_url(key: str, bucket: str = "test"):
    """Get image URL.
    Args:
        key (str): The image key.
        bucket (str): The bucket name.
    Returns:
        str: The image URL."""
    s3_client = get_s3_client()
    return s3_client.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600
    )
