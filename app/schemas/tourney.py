from typing import List

from pydantic import BaseModel, Field


class Tourney(BaseModel):
    tourney_name: str = Field(..., example='OsuChineseLeagueR Season9')
    chn_name: str = Field(None, example='中国Osu初级联赛 第九赛季')
    acronym: str = Field(None, example='OCLR S9')
    status: str = Field(None, example='Pending')
    host: int = Field(..., example=245276)
    elo_coefficient: float = Field(None, example=1)
    description: str = Field(None, example='简单介绍一下你的比赛！')


class TourneyOut(Tourney):
    staffs: List[int]
    contributor: List[int]


class AddTourneyMappoolStage(BaseModel):
    tourney_name: str = Field(..., example='oclr_s4')
    mappool_name: str = Field(..., example='oclr_s4')
    stage: str = Field(..., example='Final')
