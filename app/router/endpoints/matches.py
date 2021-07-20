from typing import List, Union

from fastapi import APIRouter, HTTPException, status, Path, Body
from fastapi.responses import ORJSONResponse

from . import make_response
from app.models import matches, elo, users
from app.core.elo import EloCalculator
from app.core.performance import SoloRule
from app.core.light_power import LightPower
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
    return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                          content=make_response('Failed',
                                                status.HTTP_404_NOT_FOUND,
                                                '未找到此场对局的信息。'))


@router.post('/{match_id}/elo',
             summary='解析比赛结果并计算ELO。',
             # response_model=MatchSchema,
             # response_class=ORJSONResponse)
             )
async def add_match_elo(*,
                        match_id: int = Path(...),
                        payload: MatchEloInSchema):
    if not (elo_festival := elo.EloFestival.get_festival(payload.elo_festival)):
        return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                              content=make_response('Failed',
                                                    status.HTTP_404_NOT_FOUND,
                                                    '未找到此ELO赛季的信息。'))
    match_response = matches.MatchResult.add_match_result(match_id, payload.elo_rule, elo_festival)
    if not match_response.get('validation'):
        return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                              content=make_response('Failed',
                                                    status.HTTP_404_NOT_FOUND,
                                                    match_response.get('message')))
    match_result = match_response.get('match_result')
    elo_change = match_result.calc_elo()
    return {k: users.User.get_user(v).username for k, v in elo_change.items()}


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


@router.post('/light_power',
             summary='计算光斗力。',
             response_class=ORJSONResponse)
async def get_light_power(*,
                          match_with_warm: List[str] = Body(..., example=['85172398/2', '84972689/2', '84896923/2'])
                          ):
    """
    统计设计
    """
    light_power = LightPower.split_warm(match_with_warm)
    return {users.User.get_user(k).username or '': v for k, v in light_power.light_power.items() if v != 0}
