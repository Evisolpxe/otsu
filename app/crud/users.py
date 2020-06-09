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


def refresh_user_raw(user_id: int):
    return get_user_by_api(user_id)[0]


def create_user(user_id: int) -> Users:
    raw_data = get_user_by_api(user_id)
    if not raw_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='官网数据库中找不到此玩家。')
    current_elo = init_elo(raw_data[0].get('pp_rank'))
    user = Users(user_id=user_id, detail=raw_data[0], current_elo=current_elo)
    user.save()
    return user


def inherit_elo(elo: schemas.users.InheritElo):
    get_user(elo.user_id)


def init_user(user_id: List[int]):
    for uid in user_id:
        user = get_user(uid)
        if user:
            user.update(detail=refresh_user_raw(uid))
        else:
            create_user(uid)
