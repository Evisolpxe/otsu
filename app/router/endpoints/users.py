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


@router.post('/user_id_translator',
             summary='User_id翻译器。')
async def user_id_translator(data: dict):
    """把user_id为key的字典丢进来，自动翻译成username"""
    if isinstance(data, dict):
        return {users.User.get_user(k).username: v for k, v in data.items()}
    raise HTTPException(406)
