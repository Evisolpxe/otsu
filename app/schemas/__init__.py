import datetime
from typing import Optional, Any

from pydantic import Field

from app.schemas.mongo import MongoModel


class ResponseSchema(MongoModel):
    status: str
    status_code: int
    message: str

