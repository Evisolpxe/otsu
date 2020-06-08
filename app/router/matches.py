from fastapi import APIRouter

from app import crud

from app.core.error import ResCode

router = APIRouter()


@router.get('/{match_id}',
            summary='获取比赛详情。')
async def get_match(*, match_id: int):
    match = crud.matches.get_match(match_id)
    if not match:
        return ResCode.raise_error(33201, match_id=match_id)
    return {'match_id': match.match_id,
            'time': str(match.time),
            'referee': match.referee,
            'stream': match.stream,
            'elo_change': match.elo_change,
            'joined_player': match.joined_player,
            'events': [{'id': event.pk,
                        'mods': event.mods,
                        'scoring_type': event.scoring_type,
                        'start_time': event.start_time,
                        'win_team': event.win_team,
                        'rank_point': event.rank_point,
                        'beatmap_id': event.beatmap_id,
                        'scores': [{'user_id': score.user_id,
                                    'accuracy': score.accuracy,
                                    'mods': score.mods,
                                    'score': score.score,
                                    'max_combo': score.max_combo,
                                    'slot': score.slot,
                                    'team': score.team,
                                    'passed': score.passed}
                                   for score in event.scores]}
                       for event in match.events]}


@router.post('/{match_id}',
             summary='添加对局。',
             response_model_exclude_unset=True,
             )
async def create_match(*, match_id: int, tourney_name: str = None, mappool_name: str = None):
    if crud.matches.get_match(match_id):
        return ResCode.raise_error(30001, match_id=match_id)
    crud.matches.create_match(match_id)
    return ResCode.raise_success(31201, match_id=match_id)


@router.delete('/{match_id}',
               summary='删除对局')
async def delete_match(*, match_id: int):
    match = crud.matches.get_match(match_id)
    if not match:
        return ResCode.raise_error(33201, match_id=match_id)
    crud.matches.delete_match(match)
    return ResCode.raise_success(41201, match_id=match_id)

@router.delete('/{match_id}/{event_id}',
               summary='删除某回合所有成绩。')
async def delete_event(event_id: int):

