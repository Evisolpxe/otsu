import json

from fastapi import APIRouter, status, Query, HTTPException, Path

from app import crud, schemas
from app.models.users import Users
from app.core.error import ResCode

router = APIRouter()


@router.get('/{user_id}',
            summary='获取玩家信息。',
            status_code=status.HTTP_200_OK)
async def get_user(*, user_id: int, refresh: bool = None):
    user = crud.users.get_user(user_id)
    if not user:
        return ResCode.raise_error(33501, user_id=user_id)
    if refresh:
        user.update(raw_data=crud.users.refresh_user_raw(user_id))
    return json.loads(user.to_json())


@router.get('/elo/{user_id}',
            summary='获取玩家ELO信息。',
            status_code=status.HTTP_200_OK)
async def get_user_elo(*, user_id: int):
    user = crud.users.get_user(user_id)
    if not user:
        return ResCode.raise_error(33501, user_id=user_id)
    elo = crud.users.get_user_elo(user_id)
    if elo:
        latest_elo = elo.elo[-1]
        r = {'elo': latest_elo.elo, 'difference': latest_elo.difference, 'match_id': latest_elo.match_id}
        if latest_elo.match_id == -1:
            r.update({'message': '本赛季您还未参加比赛哦，参加比赛或者EWC获得本赛季ELO!'})
        return r
    # elo_history = crud.users.get_elo_history(user_id)
    # if elo_history:
    #     return {'message': '本赛季您还未参加比赛哦，参加比赛或者EWC获得本赛季ELO!',
    #             'season_elo': elo_history.elo,
    #             'season_name': elo_history.season}
    return {'message': '尽快参加比赛获取ELO！'}

# @router.post('/{user_id}',
#              summary='把玩家塞进数据库。')
# async def create_user(*,
#                       user_id: int = Path(..., description='用户数字ID')
#                       ):
#     user = crud.users.get_user(user_id)
#     if user:
#         return ResCode.raise_error(12501, user_id=user_id)
#     crud.users.create_user(user_id=user_id)
#     return ResCode.raise_success(11501, user_id=user_id)


# @router.post('/{user_id}/inherit',
#              summary='继承上个赛季成绩。')
# async def inherit_elo(*,
#                       t: schemas.users.InheritElo
#                       ):
#     user = crud.users.get_user(t.user_id)
#     if user:
#         return ResCode.raise_error(12501, user_id=t.user_id)
#     user.update(elo_history=dict(t), current_elo=-1)
#     return ResCode.raise_success(21501, user_id=t.user_id)
