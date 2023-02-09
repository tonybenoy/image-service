from typing import Dict

from fastapi import Depends, FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from redis import Redis
from rq import Queue
from sqlalchemy.orm import Session

from src.config import Settings
from src.constants import IMAGE_STATUS
from src.db import Image, get_db
from src.logger import LEVELS, get_logger
from src.utils import process_image, upload_image_to_s3

redis_conn = Redis(
    host=Settings.REDIS_HOST, port=Settings.REDIS_PORT, db=Settings.REDIS_DB
)
q = Queue(Settings.RQ_QUEUE_NAME, connection=redis_conn)
app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")


logger = get_logger(__name__, LEVELS[Settings.LOG_LEVEL])


@app.get("/test", response_model=Dict[str, str])
async def test() -> Dict[str, str]:
    return {
        "result": "success",
        "msg": "It works!",
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "home": request.url_for("index"),
            "images_li": request.url_for("get_images"),
        },
    )


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
            "home": request.url_for("index"),
            "images_li": request.url_for("get_images"),
        },
    )


@app.post("/upload", response_class=HTMLResponse)
async def upload_image(
    request: Request, image: UploadFile = File(...), db: Session = Depends(get_db)
):
    """Upload image to S3."""
    logger.info("Uploading image to S3")
    if image.content_type.startswith("image/") is False:
        return templates.TemplateResponse(
            "error.html", {"request": request, "msg": "Invalid file type"}
        )
    file_name = upload_image_to_s3(image.filename, image.file, Settings.S3_BUCKET)
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
        Settings.S3_BUCKET,
    )
    logger.info("Image uploaded to S3")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "home": request.url_for("index"),
            "images_li": request.url_for("get_images"),
        },
    )


@app.get("/images", response_class=HTMLResponse)
async def get_images(request: Request, db: Session = Depends(get_db)):
    """Get all images."""
    images = db.query(Image).all()
    ims = []
    for image in images:
        ims.append(
            {
                "id": image.id,
                "name": image.name,
                "url": request.url_for("read_image", image_id=image.id),
                "processed": IMAGE_STATUS(image.processed).name,
            }
        )

    return templates.TemplateResponse(
        "images.html",
        {
            "request": request,
            "images": ims,
            "home": request.url_for("index"),
            "images_li": request.url_for("get_images"),
        },
    )
