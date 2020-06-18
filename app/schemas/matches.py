from typing import List, Dict
from pydantic import BaseModel, Field


class CreateMatch(BaseModel):
    mappool_name: str = Field(None, description='选填，会按照图池筛选对局，同时加入到图池比赛列表。不计算ELO。',
                              example="Your mappool name")
    tourney_name: str = Field(None, description='选填，会寻找对应图池筛选对局，同时加入到比赛对局。计算ELO。',
                              example='OCLB S12')
