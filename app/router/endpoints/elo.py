from typing import List, Union, Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import ORJSONResponse

from . import make_response
from app.models import matches, elo
from app.core.elo import EloCalculator
from app.core.performance import SoloRule
from app.schemas import ResponseSchema
from app.schemas.matches import MatchSchema
from app.schemas.elo import MatchEloInSchema, EloFestivalSchema

router = APIRouter()


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
