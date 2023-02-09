from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import Settings

Base = declarative_base()
engine = create_engine(Settings.DATABASE_URL)
Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


class Image(Base):  # type: ignore
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    key = Column(String, nullable=False)
    processed = Column(Integer, default=0)
    processed_key = Column(String, nullable=True)

    def get_full_url(self):
        from src.utils import get_image_url

        original_url = get_image_url(self.key)
        processed_url = (
            get_image_url(self.processed_key) if self.processed_key else None
        )
        return {"original_url": original_url, "processed_url": processed_url}
