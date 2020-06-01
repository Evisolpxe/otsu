import json

from fastapi import APIRouter, status, Query, HTTPException, Path

from app import crud, schemas
from app.models.users import Users
from app.core.error import ResCode

router = APIRouter()


@router.get('/{user_id}',
            summary='获取玩家信息。',
            status_code=status.HTTP_200_OK,
            response_model=schemas.users.User,
            response_model_exclude_unset=True)
async def get_user(*, user_id: int):
    user = crud.users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_200_OK, detail='没有获取到玩家信息哦!')
    # print(json.loads(user.to_json()))
    return json.loads(user.to_json())


@router.post('/{user_id}',
             summary='把玩家塞进数据库。')
async def create_user(*,
                      user_id: int = Path(..., description='用户数字ID'),
                      season_elo: int = Query(0, description='继承的elo.'),
                      t: schemas.users.CreateUser):
    user = crud.users.get_user(user_id)
    if user:
        return ResCode.raise_error(12501, user_id=user_id)
    crud.users.create_user(user_id=user_id, season_elo=season_elo, **dict(t))
    return ResCode.raise_success(11501, user_id=user_id)
