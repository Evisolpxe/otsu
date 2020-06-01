import json
from math import log
from typing import List

from fastapi import HTTPException, status

from app import schemas
from app.models.users import Users
from app.api.get import get_user_by_api


def init_elo(rank):
    return int(1500 - 600 * log(((int(rank) + 500) / 8500), 4))


def get_user(user_id: int) -> Users:
    return Users.objects(user_id=user_id).first()


def create_user(user_id: int, season_elo: int, **kwargs) -> Users:
    raw_data = get_user_by_api(user_id)[0]
    if season_elo == 0:
        season_elo = init_elo(raw_data.get('pp_rank'))
    user = Users(user_id=user_id, raw=raw_data, season_elo=season_elo, **kwargs)
    user.save()
    return user
