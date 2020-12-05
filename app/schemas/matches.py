import datetime
from typing import List, Set, Dict, Optional

from pydantic import Field

from app.models.mongo import MongoModel, PyObjectId


class ScoresSchema(MongoModel):
    id: PyObjectId = Field(alias="_id")
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


class GamesSchema(MongoModel):
    game_id: int = Field(...)
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime] = None
    beatmap_id: int
    play_mode: int
    match_type: int
    scoring_type: int
    mods: int
    scores: List[ScoresSchema]


class MatchSchema(MongoModel):
    match_id: int = Field(...)
    name: str
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime] = None
    games: List[GamesSchema]

    class Config:
        schema_extra = {
            'example': {
                "match_id": 70772794,
                "name": "EWC S0:(- Rainbow -) vs (Re_CYCLC)",
                "start_time": "2020-12-01T11:02:15",
                "end_time": "2020-12-01T11:29:31",
                "games": [
                    {
                        "game_id": 370370537,
                        "start_time": "2020-12-01T11:05:18",
                        "end_time": "2020-12-01T11:07:06",
                        "beatmap_id": 2321257,
                        "play_mode": 0,
                        "match_type": 0,
                        "scoring_type": 3,
                        "mods": 1,
                        "scores": [
                            {
                                "_id": "5fc9d1fe96863adcdd478571",
                                "score": 390920,
                                "user_id": 8742486,
                                "accuracy": 0,
                                "max_combo": 219,
                                "count50": 3,
                                "count100": 17,
                                "count300": 428,
                                "count_miss": 5,
                                "pass": 1,
                                "enable_mods": 0,
                                "team": 0,
                                "slot": 0
                            },
                            {
                                "_id": "5fc9d1fe96863adcdd478572",
                                "score": 357808,
                                "user_id": 9043058,
                                "accuracy": 0,
                                "max_combo": 204,
                                "count50": 1,
                                "count100": 28,
                                "count300": 413,
                                "count_miss": 11,
                                "pass": 1,
                                "enable_mods": 0,
                                "team": 0,
                                "slot": 1
                            }
                        ]
                    }
                ]
            }
        }


class GameResultSchema(MongoModel):
    game_id: int
    winner_team: int
    game_winner: List[int]
    rank_point: Dict[str, float]
    player_team: Dict[str, Set[int]]


class MatchResultSchema(MongoModel):
    match_id: int
    winner_team: int
    match_winner: List[int]
    performance_rule: str
    performance_rank: dict

    game_results: List[GameResultSchema]
