from typing import List, Union

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from app.models import matches as models
from app.core.performance import SoloRule
from app.schemas import MatchSchema

router = APIRouter()


@router.get('/{match_id}',
            summary='获取比赛基础信息，与官网保持一致。',
            # response_model=MatchSchema,
            response_class=ORJSONResponse)
async def get_match(match_id: int):
    if match := models.Match.get_match(match_id):
        return SoloRule(match=match).save_to_db()
        # return match


@router.post('/{match_id}',
             summary='解析比赛结果并计算ELO。',
             # response_model=MatchSchema,
             response_class=ORJSONResponse)
async def get_match(match_id: int, ):
    if match := models.Match.get_match(match_id):
        models.MatchResult.add_match_result(match_id, 'solo')
        # return match


@router.delete('/{match_id}',
               summary='删除比赛基础信息。',
               response_class=ORJSONResponse)
async def delete_match(match_id: int):
    return models.Match.delete_match(match_id)


@router.delete('/games/{game_id}',
               summary='删除对局基础信息。',
               response_class=ORJSONResponse)
async def delete_match_game(game_id: int):
    return models.MatchGame.delete_game(game_id)


@router.delete('/games/scores/{score_id}',
               summary='删除分数基础信息。',
               response_class=ORJSONResponse)
async def delete_match_game(score_id: int):
    return models.MatchGame.delete_game(score_id)
