from typing import Dict

from fastapi import Depends, FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from redis import Redis
from rq import Queue
from sqlalchemy.orm import Session

from src.constants import IMAGE_STATUS
from src.db import Image, get_db
from src.logger import get_logger
from src.utils import process_image, upload_image_to_s3

redis_conn = Redis(host="127.0.0.1", port=6379, db=0)
q = Queue("default", connection=redis_conn)
app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")


logger = get_logger(
    __name__,
)


@app.get("/test", response_model=Dict[str, str])
async def test() -> Dict[str, str]:
    return {
        "result": "success",
        "msg": "It works!",
    }


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload_image(
    request: Request, image: UploadFile = File(...), db: Session = Depends(get_db)
):
    """Upload image to S3."""
    logger.info("Uploading image to S3")
    file_name = upload_image_to_s3(image)
    db_image = Image(
        name=image.filename,
        key=file_name,
        processed=IMAGE_STATUS.UNPROCESSED.value,
        processed_key=None,
    )
    db.add(db_image)
    db.commit()
    q.enqueue(
        process_image,
        db_image.id,
    )
    logger.info("Image uploaded to S3")
    return templates.TemplateResponse("index.html", {"request": request})
