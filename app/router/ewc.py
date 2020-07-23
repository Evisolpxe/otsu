import json
from typing import List

from fastapi import APIRouter, status, Query, HTTPException, Path

router = APIRouter()

@router.get('/ewc/mappool')
async def get_ewc_mappool_by_players(*, players: List[int] = Query(...)):

