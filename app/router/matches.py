from fastapi import APIRouter, Query, Path, status, Depends

from app.db import models
from app.api.get import get_match_by_history

router = APIRouter()

# @router.get('/{match_id}')
# async def get_matches(*):
#     pass

@router.post('/{match_id}')
async def insert_match_into_tourney(*, match_id):
    r = get_match_by_history(match_id)
    match = models.MatchData(match_id=match_id, data=r)
    match.save()
