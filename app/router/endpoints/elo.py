from typing import List, Union

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import ORJSONResponse

from app.models import matches, elo
from app.core.elo import EloCalculator
from app.core.performance import SoloRule
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


@router.post('/elo_festival',
             summary='新建elo赛季。',
             response_model=EloFestivalSchema,
             response_class=ORJSONResponse)
async def add_elo_festival(*,
                           payload: EloFestivalSchema):
    if elo.EloFestival.get_festival(payload.name) or elo.EloFestival.get_festival(payload.acronym):
        raise HTTPException(401, detail='赛季全称或缩写重复，请检查后重试。')
    if festival := elo.EloFestival.add_festival(payload.name, payload.acronym, payload.start_time):
        return festival
