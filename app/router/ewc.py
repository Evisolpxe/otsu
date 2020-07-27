import random
from typing import List

from fastapi import APIRouter, status, Query, HTTPException, Path

from app.crud.users import get_users_avg_elo
from app.crud.mappool import get_mappool_stages_by_recommend_elo

router = APIRouter()


@router.get('/get_mappool',
            summary='通过user_id获得符合水平的图池。',
            status_code=status.HTTP_200_OK)
async def get_ewc_mappool_by_players(*, user_id_list: List[int] = Query(...)):
    elo = get_users_avg_elo(user_id_list)
    if elo:
        mappool_stage = random.choice(get_mappool_stages_by_recommend_elo(elo))
        return {'avg_elo': elo,
                'mappool': mappool_stage.mappool.mappool_name,
                'stage': mappool_stage.stage,
                'url': f'http://otsu.fun/poolDetail/{mappool_stage.mappool.acronym}'}


