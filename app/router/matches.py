from fastapi import APIRouter, BackgroundTasks

from app import crud

from app.core.error import ResCode
from app.crud.users import init_user

router = APIRouter()


@router.get('/{match_id}',
            summary='获取比赛详情。')
async def get_match(*,
                    match_id: int,
                    refresh: bool = None):
    match = crud.matches.get_match(match_id)
    if not match:
        return ResCode.raise_error(33201, match_id=match_id)
    if refresh:
        match = crud.matches.create_match(match_id)
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
async def create_match(*, match_id: int,
                       tourney_name: str = None,
                       mappool_name: str = None,
                       background_tasks: BackgroundTasks
                       ):
    if crud.matches.get_match(match_id):
        return ResCode.raise_error(30001, match_id=match_id)
    match = crud.matches.create_match(match_id)
    background_tasks.add_task(init_user, match.joined_player)
    return ResCode.raise_success(31201, match_id=match_id)


@router.delete('/{match_id}',
               summary='删除对局')
async def delete_match(*, match_id: int):
    match = crud.matches.get_match(match_id)
    if not match:
        return ResCode.raise_error(33201, match_id=match_id)
    crud.matches.delete_match(match)
    return ResCode.raise_success(41201, match_id=match_id)


@router.delete('/event/{event_id}',
               summary='删除某回合所有成绩。')
async def delete_event(event_id: int):
    event = crud.matches.get_event(event_id)
    if not event:
        return ResCode.raise_success(33202, event_id=event_id)
    crud.matches.delete_event(event)
    return ResCode.raise_success(41202, event_id=event_id)


@router.delete('/score/{score_id}',
               summary='删掉某个成绩。')
async def delete_score(score_id: str):
    score = crud.matches.get_score(score_id)
    if not score:
        return ResCode.raise_error(33203, score_id=score_id)
    crud.matches.delete_score(score)
    return ResCode.raise_success(41203, score_id=score_id)
