import uuid

import boto3
from fastapi import UploadFile

from src.constants import IMAGE_STATUS
from src.db import Image, Session


def upload_image_to_s3(image: UploadFile, bucket: str = "test"):
    """Check if image is valid and upload to S3."""
    if image.content_type.startswith("image/") is False:
        raise ValueError("File is not an image")
    filename = f"{uuid.uuid4().hex}{image.filename}"
    s3_target = boto3.client(
        "s3",
        endpoint_url="http://127.0.0.1:9000",
        aws_access_key_id="root",
        aws_secret_access_key="rootpassword",
        aws_session_token=None,
        verify=False,
    )
    s3_target.upload_fileobj(image.file, bucket, filename)
    return filename


def process_image(img_id: int):
    """Process image."""
    db = Session()
    image = (
        db.query(Image)
        .filter(Image.id == img_id, Image.processed == IMAGE_STATUS.UNPROCESSED.value)
        .first()
    )
    if not image:
        return
    # TODO: Process image  # pylint: disable=fixme
    image.processed = IMAGE_STATUS.PROCESSED.value
    image.processed_key = "processed"
    db.commit()
    return
