from typing import List, Dict
from pydantic import BaseModel, Field


class User(BaseModel):
    detail: dict
    season_elo: int = Field(None)
    current_elo: int = Field(None)


class CreateUser(BaseModel):
    """
    elo_history: {'season0': 1200, 'season1': 1500}
    """
    # elo_history: List[dict] = Field([{'user_id': 0, 'elo': 1000, 'season': '0'}])
    pass


class InheritElo(BaseModel):
    user_id: int
    elo: int
    season: str
