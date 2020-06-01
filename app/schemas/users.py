from typing import List, Dict
from pydantic import BaseModel, Field


class User(BaseModel):
    raw: dict
    season_elo: int
    current_elo: int = Field(None)


class CreateUser(BaseModel):
    elo_history: Dict = Field(None)
