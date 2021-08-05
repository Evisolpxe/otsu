from typing import List, Union, Optional

from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import ORJSONResponse

from . import make_response
from app.models import matches, elo
from app.core.elo import EloCalculator
from app.core.performance import SoloRule
from app.schemas import ResponseSchema
from app.schemas.matches import MatchSchema
from app.schemas.elo import MatchEloInSchema, EloFestivalSchema
from app.schemas.elo import UserEloSchema, EloChangeSchema, UserRankingSchema

router = APIRouter()


@router.get('/ranking',
            summary='获取elo排行榜',
            response_model=List[UserRankingSchema],
            response_class=ORJSONResponse
            )
async def get_ranking(elo_festival: str,
                      country: str = None,
                      per_page: int = 50,
                      num_page: int = 1,
                      ):
    return elo.UserRanking.get_ranking(elo_festival, country, per_page=per_page, num_page=num_page)


@router.get('/{user_id}',
            summary='获取玩家所有种类elo信息。',
            response_model=Union[List[UserEloSchema], UserEloSchema],
            response_class=ORJSONResponse)
async def get_user(user_id: int, elo_festival: str = None):
    if user := elo.UserElo.get_user_elo(user_id, elo_festival):
        return user
    return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                          content=make_response('Failed',
                                                status.HTTP_404_NOT_FOUND,
                                                '未找到elo_festival或者没有这位玩家的信息哦。'))


@router.get('/{user_id}/recent',
            summary='获取最近elo变动场次，默认5场。',
            response_model=List[EloChangeSchema],
            response_class=ORJSONResponse)
async def get_user_recent(user_id: int, elo_festival: str, num: int = Query(5)):
    if user := elo.UserElo.get_user_elo(user_id, elo_festival):
        return [i for i in user.elo_change_list][:num]
    return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                          content=make_response('Failed',
                                                status.HTTP_404_NOT_FOUND,
                                                '未找到elo_festival或者没有这位玩家的信息哦。'))


@router.get('/{user_id}/ranking',
            summary='获得elo排名，并且返回前后N名玩家的id。',
            response_model=List[UserRankingSchema],
            response_class=ORJSONResponse)
async def get_user_ranking(user_id: int,
                           elo_festival: str,
                           country: str,
                           # per_page: int = 50,
                           # num_page: int = 1,
                           num_neighbor: int = 2):
    if not elo.UserElo.get_user_elo(user_id, elo_festival):
        return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                              content=make_response('Failed',
                                                    status.HTTP_404_NOT_FOUND,
                                                    '未找到elo_festival或者没有这位玩家的信息哦。'))
    return elo.UserRanking.get_ranking(elo_festival, country, user_id, num_neighbor=num_neighbor)


@router.get('/elo_festival',
            summary='获得elo赛季信息。',
            response_model=EloFestivalSchema,
            response_class=ORJSONResponse)
async def add_elo_festival(*,
                           name: str):
    if festival := elo.EloFestival.get_festival(name):
        return festival
    return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                          content=make_response('Failed',
                                                status.HTTP_404_NOT_FOUND,
                                                '未找到此ELO赛季的信息。'))


@router.post('/elo_festival',
             summary='新建elo赛季。',
             response_model=EloFestivalSchema,
             response_class=ORJSONResponse)
async def add_elo_festival(*,
                           payload: EloFestivalSchema):
    if elo.EloFestival.get_festival(payload.name) or elo.EloFestival.get_festival(payload.acronym):
        return ORJSONResponse(status_code=status.HTTP_409_CONFLICT,
                              content=make_response('Failed',
                                                    status.HTTP_409_CONFLICT,
                                                    '赛季全称或缩写重复，请检查后重试。'))
    if elo.EloFestival.add_festival(payload.name, payload.acronym, payload.start_time):
        return ORJSONResponse(status_code=status.HTTP_201_CREATED,
                              content=make_response('Success',
                                                    status.HTTP_201_CREATED,
                                                    '创建比赛成功。'))
