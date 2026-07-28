from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime

from datetime import datetime

from src.database.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)

    filename = Column(String, nullable=False)

    upload_time = Column(
        DateTime,
        default=datetime.utcnow
    )

    total_pages = Column(
        Integer,
        default=0
    )

    total_chunks = Column(
        Integer,
        default=0
    )

    processing_status = Column(
        String,
        default="PENDING"
    )

    category = Column(
        String,
        default="Unknown"
    )