import json
from typing import List

from fastapi import APIRouter, status, Query, Path, HTTPException, Response

from app.models.maps import MapData
from app.crud.maps import get_beatmap
from app.core.error import ResCode

router = APIRouter()


@router.get('/{beatmap_id}',
            summary='返回beatmap信息')
async def get_beatmaps(*,
                       beatmap_id: int,
                       mod: str = Query('NM', description='DT, HR, EZ, HT可选。'),
                       refresh: bool = False):
    return get_beatmap(beatmap_id, mod=mod, refresh=refresh)
