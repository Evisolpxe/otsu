from typing import List
from pydantic import BaseModel, Field


class MappoolRatingCount(BaseModel):
    avg: float
    counts: int


class MappoolRating(MappoolRatingCount):
    user_id_list: List[int]


class MappoolComment(BaseModel):
    user_id: int = Field(..., description='评论人uid', exmaple=245276)
    content: str = Field('好评如潮。', description='评论。', example='好评如潮。')
    reply: int = Field(None, description='回复楼层, 评论的comment_id。', example=0)


class CreateMappool(BaseModel):
    mappool_name: str = Field(example='OsuChineseLeagueR Season11')
    host: int = Field(..., description='图池的创建者，无法修改。', example=245276)
    recommend_elo: int = Field(..., description='创建者推荐适合的elo范围。', ge=0, le=3000, example=1000)
    cover: int = Field(..., description='主页现实的图池封面，初始为0，在第一次传图后设为图池第一张图，之后可以自己设置。')
    description: str = Field(..., description='创建者对图池的简介。',
                             example='## This is a description. #### You can write it by Markdown.')


class GetMappool(CreateMappool):
    status: str = Field(example='Pending')

    rating: MappoolRating
    comments


class UpdateMappool(BaseModel):
    recommend_elo: int = Field(..., description='创建者推荐适合的elo范围。', ge=0, le=3000, example=1000)
    cover: int = Field(..., description='主页现实的图池封面，初始为0，在第一次传图后设为图池第一张图，之后可以自己设置。')
    description: str = Field(..., description='创建者对图池的简介。',
                             example='## This is a description. #### You can write it by Markdown.')
    status: str = Field(example='Pending')


class MappoolOverview(CreateMappool):
    status: str = Field(example='Pending')
    rating: MappoolRatingCount
