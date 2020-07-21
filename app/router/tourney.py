import json

from fastapi import APIRouter, status, Query, HTTPException

from app import crud, schemas
from app.core.error import ResCode

router = APIRouter()


@router.get('/{tourney_name}',
            summary='获取比赛。',
            status_code=status.HTTP_200_OK)
async def get_tourney(*,
                      tourney_name: str = Query(..., description='比赛名称，支持中文名、缩写、全称。')
                      ):
    q = crud.tourney.get_tourney(tourney_name)
    if not q:
        return ResCode.raise_error(32101, tourney_name=tourney_name)
    return {"tourney_name": q.tourney_name,
            "chn_name": q.chn_name,
            "acronym": q.acronym,
            "status": q.status,
            "elo_coefficient": q.elo_coefficient,
            "performance_rule": q.performance_rule,
            "description": q.description,
            "host": q.host,
            "staffs": q.staffs,
            "contributor": q.contributor,
            "matches": [s.match_id for s in q.matches],
            "mappool_stages": [s.stage for s in q.mappool_stages]
            }


@router.get('/{tourney_name}/statistics',
            summary='关于比赛的各种数据。',
            description='说明晚点写。')
async def get_tourney_statistics(*, tourney_name: str):
    q = crud.tourney.get_tourney(tourney_name)
    if not q:
        return ResCode.raise_error(32101, name=tourney_name)




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
        return ResCode.raise_error(12101,
                                   tourney_name=q.tourney_name,
                                   acronym=q.acronym,
                                   chn_name=q.chn_name)
    crud.tourney.create_tourney(t)
    return ResCode.raise_success(11101, tourney_name=t.tourney_name, host=t.host)


@router.post('/{tourney_name}/',
             summary='将某个MappoolStage添加至比赛。',
             status_code=status.HTTP_201_CREATED)
async def add_stage_to_tourney(*,
                               t: schemas.tourney.AddTourneyMappoolStage
                               ) -> schemas.RaiseInfo:
    tourney = crud.tourney.get_tourney(t.tourney_name)
    if not tourney:
        return ResCode.raise_error(32101, tourney_name=t.tourney_name, )
    q = crud.mappool.get_mappool(t.mappool_name)
    if not q:
        return ResCode.raise_error(32301, mappool_name=t.mappool_name)
    stage = crud.mappool.get_mappool_stage(q, t.stage)
    if not stage:
        return ResCode.raise_error(32305, stage=stage)
    if stage in tourney.mappool_stages:
        return ResCode.raise_error(12102)
    crud.tourney.add_mappool_stage_to_tourney(tourney, stage)
    return ResCode.raise_success(11102, tourney=t.tourney_name, stage=t.stage)
