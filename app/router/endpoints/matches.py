from typing import List, Union

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from ...models import matches as models
from ...schemas import PublicResponseSchema, MatchSchema

router = APIRouter()


@router.get('/{match_id}',
            summary='获取比赛基础信息，与官网保持一致。',
            response_model=MatchSchema,
            response_class=ORJSONResponse)
async def get_match(match_id: int):
    if match := models.Match.get_match(match_id):
        return match.to_dict()


@router.delete('/{match_id}',
               summary='删除比赛基础信息。',
               response_class=ORJSONResponse)
async def get_match(match_id: int):
    return models.Match.delete_match(match_id)
