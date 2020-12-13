from typing import List, Union

from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

from app.models import matches, elo, users
from app.core.elo import EloCalculator
from app.core.performance import SoloRule
from app.schemas import UserEloSchema

router = APIRouter()


@router.get('/{user_id}',
            summary='获取比赛基础信息，与官网保持一致。',
            response_model=UserEloSchema,
            response_class=ORJSONResponse)
async def get_user(user_id: int):
    if user := elo.UserElo.get_user_elo(user_id):
        return user
    raise HTTPException(404, detail={'message': '没有这位玩家的信息哦。'})
