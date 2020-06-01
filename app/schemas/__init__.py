from pydantic import BaseModel
from . import tourney, mappool, users


class RaiseInfo(BaseModel):
    message: str
    code: int
    time: str
    status: int
