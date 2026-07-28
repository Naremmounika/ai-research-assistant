from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    id: str
    filename: str
    upload_time: datetime
    processing_status: str

    class Config:
        from_attributes = True