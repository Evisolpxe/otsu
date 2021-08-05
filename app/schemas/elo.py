import datetime
from typing import Optional, Any

from pydantic import Field

from app.schemas.mongo import MongoModel


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


class UserRankingSchema(MongoModel):
    user_id: int
    username: str
    country: str
    rank: int
    country_rank: int
    current_elo: int
    play_counts: int

    class Config:
        schema_extra = {
            'example': {
                'username': 'Crystal',
                'rank': 1,
                'current_elo': 99999
            }
        }


class UserEloSchema(MongoModel):
    user_id: int
    elo_festival: EloFestivalSchema
    current_elo: int
    init_elo: int


class EloChangeSchema(MongoModel):
    match_id: int
    difference: int
