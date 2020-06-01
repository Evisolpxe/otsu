import json

from fastapi import APIRouter, status, Query, HTTPException

from app import crud, schemas
from app.core.error import ResCode

router = APIRouter()


@router.get('/{tourney_name}',
            summary='获取比赛。',
            status_code=status.HTTP_200_OK,
            response_model=schemas.tourney.TourneyOut,
            response_model_exclude_unset=True)
async def get_tourney(*,
                      name: str = Query(..., description='比赛名称，支持中文名、缩写、全称。')
                      ) -> schemas.tourney.TourneyOut:
    q = crud.tourney.get_tourney(name)
    if not q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='没有找到对应比赛哦！')
    return json.loads(q.to_json())


@router.post('/{tourney_name}',
             summary='创建比赛。',
             status_code=status.HTTP_201_CREATED)
async def create_tourney(*,
                         t: schemas.tourney.Tourney
                         ) -> schemas.RaiseInfo:
    q = crud.tourney.get_tourney(name=t.tourney_name) \
        or crud.tourney.get_tourney(name=t.acronym) \
        or crud.tourney.get_tourney(name=t.chn_name)
    if q:
        return ResCode.raise_error(12101, info={'tourney_name': q.tourney_name,
                                                'acronym': q.acronym,
                                                'chn_name': q.chn_name})
    crud.tourney.create_tourney(t)
    return ResCode.raise_success(11101, tourney_name=t.tourney_name, host=t.host)
