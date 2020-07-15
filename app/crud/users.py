import json
from math import log
from typing import List

from fastapi import HTTPException, status

from app import schemas
from app.models.users import Users, Elo, EloHistory
from app.api.get import get_user_by_api


def init_elo(rank):
    return int(1500 - 600 * log(((int(rank) + 500) / 8500), 4))


def get_user(user_id: int) -> Users:
    return Users.objects(user_id=user_id).first()


def get_user_elo(user_id: int):
    return Elo.objects(user_id=user_id).order_by('-match_id').first()


def refresh_user_raw(user_id: int):
    return get_user_by_api(user_id)[0]


def create_user(user_id: int) -> Users:
    raw_data = get_user_by_api(user_id)
    if not raw_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='官网数据库中找不到此玩家。')
    current_elo = init_elo(raw_data[0].get('pp_rank'))
    elo_history = get_elo_history(user_id)
    if elo_history:
        current_elo = elo_history.elo
    elo = Elo(user_id=user_id, elo=current_elo)
    elo.save()
    user = Users(user_id=user_id, detail=raw_data[0])
    user.save()
    user.update(push__elo=elo)
    if elo_history:
        user.update(push__elo_history=elo_history)
    return user


def get_elo_history(user_id: int) -> EloHistory:
    return EloHistory.objects(user_id=user_id).order_by('-add_time').first()


def inherit_elo(elo: schemas.users.InheritElo):
    get_user(elo.user_id)


def init_user(user_id: List[int], refresh=False):
    for uid in user_id:
        user = get_user(uid)
        if user:
            if refresh:
                user.update(detail=refresh_user_raw(uid))
        else:
            try:
                create_user(uid)
            except Exception as e:
                print(e)
