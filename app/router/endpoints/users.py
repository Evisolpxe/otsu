from typing import List, Union

from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

from app.models import matches, elo, users
from app.core.elo import EloCalculator
from app.core.performance import SoloRule
from app.schemas.users import UserEloSchema

router = APIRouter()


@router.get('/{user_id}',
            summary='获取玩家elo信息。',
            response_model=UserEloSchema,
            response_class=ORJSONResponse)
async def get_user(user_id: int, elo_festival: str):
    if user := elo.UserElo.get_user_elo(user_id, elo_festival):
        return user
    raise HTTPException(404, detail={'message': '没有这位玩家的信息哦。'})
