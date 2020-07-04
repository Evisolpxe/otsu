from datetime import datetime

from typing import List, Dict
from pydantic import BaseModel, Field


class MappoolRatingCount(BaseModel):
    avg: float
    counts: int


class MappoolRating(MappoolRatingCount):
    user_id: List[int]


class CreateMappoolRating(BaseModel):
    user_id: int
    rating: int


class MappoolComment(BaseModel):
    user_id: int = Field(..., description='评论人uid', exmaple=245276)
    content: str = Field('好评如潮。', description='评论。', example='好评如潮。')
    reply: str = Field(None, description='回复楼层, 评论的comment_id，无回复请返回空字符。', example="")


class MappoolCommentOut(MappoolComment):
    comment_id: str
    timestamp: str


class CreateMappool(BaseModel):
    mappool_name: str = Field(..., example='OsuChineseLeagueR Season11')
    acronym: str = Field(..., example='OCLR_S11', description='只允许数字、字母、下划线。')
    host: int = Field(..., description='图池的创建者，无法修改。', example=245276)
    recommend_elo: List[int] = Field(..., description='创建者推荐适合的elo范围。', example=[600, 1000])
    cover: int = Field(..., description='主页现实的图池封面，初始为0，在第一次传图后设为图池第一张图，之后可以自己设置。')
    mappool_date: datetime = Field(None, description='图池出炉日期，可以不填。', alias='date')
    description: str = Field(..., description='创建者对图池的简介。',
                             example='## This is a description. #### You can write it by Markdown.')


class GetMappool(CreateMappool):
    status: str = Field(example='Pending')

    rating: MappoolRating
    comments: List[MappoolComment]


class UpdateMappool(BaseModel):
    mappool_name: str = None
    acronym: str = Field(..., example='OCLR_S11', description='只允许数字、字母、下划线。')
    recommend_elo: List[int] = Field(None, description='创建者推荐适合的elo范围。', example=[600, 1000])
    cover: int = Field(None, description='主页现实的图池封面，初始为0，在第一次传图后设为图池第一张图，之后可以自己设置。')
    description: str = Field(None, description='创建者对图池的简介。',
                             example='## This is a description. #### You can write it by Markdown.')
    mappool_date: datetime = Field(None, description='图池出炉日期，可以不填。', alias='date')
    status: str = Field(None, example='Pending')


class MappoolOverview(CreateMappool):
    status: str = Field(example='Pending')
    stages: List[str] = None
    rating: MappoolRatingCount


class MappoolMap(BaseModel):
    beatmap_id: int = Field(..., example=48416, ge=1)
    mod_index: int = Field(..., example=1, ge=1)
    selector: int = Field(None, example=245276)
    mods: List[str] = Field(..., example=['DT'])


class MappoolMapOut(MappoolMap):
    object_id: str
    detail: dict


class MappoolStage(BaseModel):
    stage: str = Field(..., example='SemiFinal')
    recommend_elo: List[int] = Field(..., example=[600, 1000])
