import datetime
from typing import List, Dict, Optional

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
    pass_: int = Field(alias='pass')
    enable_mods: int
    team: int
    slot: int


class GamesSchema(BaseModel):
    game_id: int = Field(...)
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime] = None
    beatmap_id: int
    play_mode: int
    match_type: int
    scoring_type: int
    mods: int
    scores: List[ScoresSchema]


class MatchSchema(BaseModel):
    match_id: int = Field(...)
    name: str
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime] = None
    games: List[GamesSchema]

    class Config:
        schema_extra = {
            'example': {
                "match_id": 66160343,
                "name": "4WC: (China) vs (Australia)",
                "start_time": "2020-08-29T09:53:26",
                "end_time": "2020-08-29T11:14:19",
                "games": [
                    {
                        "game_id": 346638012,
                        "start_time": "2020-08-29T10:06:32",
                        "end_time": "2020-08-29T10:09:34",
                        "beatmap_id": 2292446,
                        "play_mode": 0,
                        "match_type": 0,
                        "scoring_type": 3,
                        "mods": 0,
                        "scores": [
                            {
                                "user_id": 5791401,
                                "score": 928370,
                                "accuracy": 0,
                                "max_combo": 979,
                                "count50": 1,
                                "count100": 25,
                                "count300": 729,
                                "count_miss": 0,
                                "pass": 1,
                                "enable_mods": 0,
                                "team": 1,
                                "slot": 0
                            },
                            {
                                "user_id": 7839397,
                                "score": 215955,
                                "accuracy": 0,
                                "max_combo": 193,
                                "count50": 5,
                                "count100": 49,
                                "count300": 678,
                                "count_miss": 23,
                                "pass": 1,
                                "enable_mods": 0,
                                "team": 1,
                                "slot": 1
                            },
                            {
                                "user_id": 6090175,
                                "score": 291737,
                                "accuracy": 0,
                                "max_combo": 315,
                                "count50": 1,
                                "count100": 102,
                                "count300": 647,
                                "count_miss": 5,
                                "pass": 1,
                                "enable_mods": 0,
                                "team": 1,
                                "slot": 2
                            },
                            {
                                "user_id": 9240047,
                                "score": 84096,
                                "accuracy": 0,
                                "max_combo": 109,
                                "count50": 7,
                                "count100": 198,
                                "count300": 522,
                                "count_miss": 28,
                                "pass": 1,
                                "enable_mods": 16,
                                "team": 2,
                                "slot": 4
                            },
                            {
                                "user_id": 11076938,
                                "score": 165109,
                                "accuracy": 0,
                                "max_combo": 121,
                                "count50": 4,
                                "count100": 98,
                                "count300": 634,
                                "count_miss": 19,
                                "pass": 1,
                                "enable_mods": 16,
                                "team": 2,
                                "slot": 6
                            }
                        ]
                    }
                ]
            },

        }
