from fastapi import APIRouter, BackgroundTasks, Query

from app import crud
from app.schemas.matches import CreateMatch

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
                       t: CreateMatch,
                       background_tasks: BackgroundTasks
                       ):
    if crud.matches.get_match(match_id):
        return ResCode.raise_error(30001, match_id=match_id)

    match = crud.matches.create_match(match_id)
    if not match:
        return ResCode.raise_error(34201, match_id=match_id)
    background_tasks.add_task(init_user, match.joined_player)

    if t.mappool_name:
        mappool = crud.mappool.get_mappool(t.mappool_name)
        if not mappool:
            return ResCode.raise_error(12301, mappool_name=t.mappool_name)
        crud.matches.push_match_to_mappool(mappool, match)

    if t.tourney_name:
        tourney = crud.tourney.get_tourney(t.tourney_name)
        if not tourney:
            return ResCode.raise_error(32101, tourney_name=t.tourney_name)
        crud.matches.push_match_to_tourney(tourney, match)

    return ResCode.raise_success(31201, match_id=match_id)


@router.delete('/{match_id}',
               summary='删除对局')
async def delete_match(*, match_id: int):
    match = crud.matches.get_match(match_id)
    if not match:
        return ResCode.raise_error(33201, match_id=match_id)
    crud.matches.delete_match(match)
    return ResCode.raise_success(41201, match_id=match_id)


@router.post('/{match_id}/mappool',
             summary='把比赛添加到图池，并把成绩按照图池过滤。')
async def match_filter_by_mappool(*,
                                  match_id: int,
                                  mappool_name: str):
    match = crud.matches.get_match(match_id)
    if not match:
        return ResCode.raise_error(33201, match_id=match_id)

    mappool = crud.mappool.get_mappool(mappool_name)
    if not mappool:
        return ResCode.raise_error(32301, mappool_name=mappool_name)

    crud.matches.push_match_to_mappool(mappool, match)
    return ResCode.raise_success(31221)


@router.post('/{match_id}/tourney',
             summary='把比赛添加到比赛，并把成绩按照比赛图池过滤。')
async def match_filter_by_tourney(*,
                                  match_id: int,
                                  tourney_name: str):
    match = crud.matches.get_match(match_id)
    if not match:
        return ResCode.raise_error(33201, match_id=match_id)

    tourney = crud.tourney.get_tourney(tourney_name)
    if not tourney:
        return ResCode.raise_error(32101, tourney_name=tourney_name)

    crud.matches.push_match_to_tourney(tourney, match)
    return ResCode.raise_success(31211)


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


@router.post('/calc/{break_point_id}',
             summary='计算elo')
async def calc_elo(break_point_id: int = Query(...)):
    match = crud.matches.calc_all_elo(break_point_id)
    return ResCode.raise_success(31200, calc_length=match)
