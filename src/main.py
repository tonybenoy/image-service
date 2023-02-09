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


@app.get("/image/{image_id}", response_class=HTMLResponse)
async def read_image(request: Request, image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if not db_image:
        return templates.TemplateResponse("index.html", {"request": request})
    return templates.TemplateResponse(
        "image.html",
        {
            "request": request,
            "image": db_image.get_full_url(),
        },
    )


@app.post("/upload", response_class=HTMLResponse)
async def upload_image(
    request: Request, image: UploadFile = File(...), db: Session = Depends(get_db)
):
    """Upload image to S3."""
    logger.info("Uploading image to S3")
    if image.content_type.startswith("image/") is False:
        raise ValueError("File is not an image")
    file_name = upload_image_to_s3(image.filename, image.file, "test")
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
