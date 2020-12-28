import datetime
from typing import List, Set, Dict, Optional, Any

from pydantic import Field

from app.models.mongo import MongoModel, PyObjectId
from app.festivals import EloFestivalEnum
from app.rules import PerformanceEnum


class MatchEloInSchema(MongoModel):
    elo_rule: str = Field(...)
    elo_festival: str = Field(...)
    warm_up: int = 0
    map_pool: Optional[str] = None

    def __init__(self, **data: Any):
        super().__init__(**data)

    class Config:
        schema_extra = {
            'example': {
                'elo_rule': 'solo',
                'elo_festival': 'wild',
                'warm_up': 0,
                'map_pool': ''
            }
        }


class EloFestivalSchema(MongoModel):
    name: str = Field(...)
    acronym: str = Field(...)
    start_time: datetime.datetime = Field(...)
    end_time: datetime.datetime = None
    status: str = None

    class Config:
        schema_extra = {
            'example': {
                'name': 'EloWeeklyCup Season1',
                'acronym': 'EWC S1',
                'start_time': '2020-12-25 00:00',
                'end_time': '2021-01-03 00:00',
            }
        }
