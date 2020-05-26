import json
from typing import List

from fastapi import APIRouter, status, Query, Path, HTTPException

from app import models, crud, schemas
from app.core.error import raise_error, raise_success

router = APIRouter()


@router.get('/',
            summary='获取全部图池概况，可分页。',
            status_code=status.HTTP_200_OK,
            response_model=List[schemas.mappool.MappoolOverview])
async def get_all_mappool(*,
                          pagination: bool = False, page: int = 0, per_page: int = 30
                          ) -> List[schemas.mappool.MappoolOverview]:
    q_list = crud.mappool.get_all_mappool()
    if q_list:
        if pagination:
            start = page * per_page
            end = start + per_page
            q_list = q_list[start: end]

        q_overview = []
        for q in q_list:
            overview = json.loads(q.to_json())
            overview.update({'rating': crud.mappool.calc_rating(q.ratings)})
            q_overview.append(overview)
        return q_overview
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='还没有任何图池QwQ...快快上传吧!')


@router.post('/',
             summary='创建新图池。',
             status_code=status.HTTP_201_CREATED)
async def create_mappool(*,
                         t: schemas.mappool.CreateMappool
                         ) -> schemas.RaiseInfo:
    q = crud.mappool.get_mappool(t.mappool_name)
    if q:
        return raise_error(30005, mappool_name=t.mappool_name)

    crud.mappool.create_mappool(t)
    return raise_success(10003, mappool_name=t.mappool_name)


@router.get('/{mappool_name}',
            summary='获取图池信息。',
            status_code=status.HTTP_200_OK,
            response_model=None,
            response_model_exclude_unset=True,
            )
async def get_mappool(*,
                      mappool_name: str = Path(..., description='图池名称，只支持全称查询。')
                      ) -> schemas.mappool.MappoolOverview:
    q = crud.mappool.get_mappool(mappool_name)
    if q:
        return json.loads(q.to_json())
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='没有找到对应图池哦！')


@router.put('/{mappool_name}')
async def update_mappool(*,
                         mappool_name: str = Path(..., description='图池名称，只支持全称查询。')
                         ):
    pass
