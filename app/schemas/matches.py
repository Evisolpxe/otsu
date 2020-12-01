import datetime
from typing import List, Dict

from pydantic import BaseModel, Field


class ScoresSchema(BaseModel):
    user_id: int
    score: int
    user_id: int
    score: int
    accuracy: int
    max_combo: int
    count50: int
    count100: int
    count300: int
    count_miss: int
    pass_: int
    enable_mods: int
    team: int
    slot: int


class GamesSchema(BaseModel):
    game_id: int = Field(...)
    start_time: datetime.datetime
    end_time: datetime.datetime
    beatmap_id: int
    play_mode: int
    match_type: int
    scoring_type: int
    mods: int
    # scores: List[ScoresSchema]


class MatchSchema(BaseModel):
    match_id: int = Field(...)
    name: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    # games: List[GamesSchema]

    class Config:
        schema_extra = {
            'example': {
                'id': 70772794,
                'name': 'EWC S0:(- Rainbow -) vs (Re_CYCLC)',
                'start_time': datetime.datetime.utcnow().replace(microsecond=0),
                'end_time': datetime.datetime.utcnow().replace(microsecond=0) + datetime.timedelta(days=2),
                'games': [370370537, 370371307, 370371703, 370371987, 370372349, 370372802, 370373221]
            },

        }
