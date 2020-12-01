import orjson
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from app.models import matches as models

router = APIRouter()


@router.get('/{match_id}',
            summary='获取比赛基础信息。',
            response_class=ORJSONResponse)
async def get_match(match_id: int):
    match := models.Match.get_match(match_id)

    return response
