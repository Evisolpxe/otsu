from typing import List, Union

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import ORJSONResponse

from . import make_response
from app.models import matches, elo, users
from app.core.elo import EloCalculator
from app.core.performance import SoloRule

router = APIRouter()


@router.post('/user_id_translator',
             summary='User_id翻译器。')
async def user_id_translator(data: dict):
    """把user_id为key的字典丢进来，自动翻译成username"""
    if isinstance(data, dict):
        return {users.User.get_user(k).username or '': v for k, v in data.items()}
    raise HTTPException(406)


@router.post('/username_translator',
             summary='Username翻译器。')
async def user_id_translator(data: List[str]):
    """把username丢进来，自动翻译成user_id"""
    if isinstance(data, list):
        return [users.User.get_user(username=k).user_id for k in data]
    raise HTTPException(406)
