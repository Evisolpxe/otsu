from typing import List, Union

from fastapi import APIRouter, HTTPException, status, Path
from fastapi.responses import ORJSONResponse

from app.models import matches, elo
from app.core.elo import EloCalculator
from app.core.performance import SoloRule
from app.schemas.matches import MatchSchema
from app.schemas.elo import MatchEloInSchema

router = APIRouter()


@router.get('/{match_id}',
            summary='获取比赛基础信息，与官网保持一致。',
            response_model=MatchSchema,
            response_class=ORJSONResponse)
async def get_match(match_id: int):
    if match := matches.Match.get_match(match_id):
        return match


@router.post('/{match_id}/elo',
             summary='解析比赛结果并计算ELO。',
             # response_model=MatchSchema,
             # response_class=ORJSONResponse)
             )
async def add_match_elo(*,
                        match_id: int = Path(...),
                        payload: MatchEloInSchema):
    if not (elo_festival := elo.EloFestival.get_festival(payload.elo_festival)):
        raise HTTPException(404, detail='未找到festival信息!')
    match_response = matches.MatchResult.add_match_result(match_id, payload.elo_rule, elo_festival)
    if not match_response.get('validation'):
        return match_response
    match_result = match_response.get('match_result')
    elo_change = match_result.calc_elo()
    return elo_change


@router.delete('/{match_id}',
               summary='删除比赛基础信息。',
               response_class=ORJSONResponse)
async def delete_match(match_id: int):
    return matches.Match.delete_match(match_id)


@router.delete('/games/{game_id}',
               summary='删除对局基础信息。',
               response_class=ORJSONResponse)
async def delete_match_game(game_id: int):
    return matches.MatchGame.delete_game(game_id)


@router.delete('/games/scores/{score_id}',
               summary='删除分数基础信息。',
               response_class=ORJSONResponse)
async def delete_match_game(score_id: int):
    return matches.MatchGame.delete_game(score_id)
