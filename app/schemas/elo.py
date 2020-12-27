from typing import List, Set, Dict, Optional, Any

from pydantic import Field

from app.models.mongo import MongoModel, PyObjectId
from app.festivals import EloFestivalEnum
from app.rules import PerformanceEnum


class MatchEloInSchema(MongoModel):
    match_id: int = Field(...)
    elo_rule: str = Field(...)
    elo_festival: str = Field(...)
    warm_up: int = 0
    map_pool: Optional[str] = None

    def __init__(self, **data: Any):
        super().__init__(**data)

    class Config:
        schema_extra = {
            'example': {
                'match_id': 64389206,
                'elo_rule': 'solo',
                'elo_festival': 'wild',
                'warm_up': 0,
                'map_pool': ''
            }
        }
