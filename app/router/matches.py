from fastapi import APIRouter

from app import models
from app.api.get import get_match_by_history

from app.core.error import raise_error

router = APIRouter()


# @router.get('/{match_id}')
# async def get_matches(*):
#     pass


@router.post('/{match_id}',
             summary='添加场次。',
             response_model_exclude_unset=True,
             )
async def insert_match_into_tourney(*, match_id: int, tourney_name: str):
    if models.MatchData.objects(match_id=match_id):
        return raise_error(30001, match_id=match_id)

    r = get_match_by_history(match_id)
    match = models.MatchData(match_id=match_id, data=r)
    match.save()
