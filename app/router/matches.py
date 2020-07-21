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
    r = {'match_id': match.match_id,
         'time': str(match.time),
         'referee': match.referee,
         'stream': match.stream,
         'elo_change': {i.user_id: i.difference for i in match.elo_change},
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
    win_counts = [i.get('win_team') for i in r['events']]
    r.update({'blue_win': win_counts.count('blue'), 'red_win': win_counts.count('red')})
    return r


@router.post('/{match_id}',
             summary='添加对局。',
             response_model_exclude_unset=True,
             deprecated=True
             )
async def create_match(*,
                       match_id: int,
                       t: CreateMatch,
                       background_tasks: BackgroundTasks
                       ):
    if crud.matches.get_match(match_id):
        return ResCode.raise_error(32201, match_id=match_id)

    match_data = crud.matches.create_match(match_id)
    if not match_data:
        return ResCode.raise_error(34201, match_id=match_id)

    if t.mappool_name or t.tourney_name:
        match = crud.matches.parse_match(match_id, match_data)

    if t.mappool_name:
        mappool = crud.mappool.get_mappool(t.mappool_name)
        if not mappool:
            return ResCode.raise_error(32301, mappool_name=t.mappool_name)
        crud.matches.push_match_to_mappool(mappool, match)

    if t.tourney_name:
        tourney = crud.tourney.get_tourney(t.tourney_name)
        if not tourney:
            return ResCode.raise_error(32101, tourney_name=t.tourney_name)
        crud.matches.push_match_to_tourney(tourney, match)

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


@router.post('/{match_id}/mappool',
             summary='把对局添加到图池，并把成绩按照图池过滤。')
async def match_filter_by_mappool(*,
                                  match_id: int = Query(...),
                                  mappool_name: str = Query(...),
                                  stage: str = Query(..., description='Stage名称'),
                                  background_tasks: BackgroundTasks):
    if crud.matches.get_match(match_id):
        return ResCode.raise_error(32201, match_id=match_id)

    match_data = crud.matches.create_match(match_id)
    if not match_data:
        return ResCode.raise_error(34201, match_id=match_id)

    mappool = crud.mappool.get_mappool(mappool_name)
    if not mappool:
        return ResCode.raise_error(32301, mappool_name=mappool_name)

    s = crud.mappool.get_mappool_stage(mappool, stage)
    if not s:
        return ResCode.raise_error(32305, stage=stage)

    match = crud.matches.parse_match(match_id, match_data)
    r = crud.matches.push_match_to_mappool(s, match)
    if r.get('total_events') == r.get('removed_events'):
        crud.matches.delete_match(match)
        return ResCode.raise_error(32211)
    background_tasks.add_task(init_user, match.joined_player)

    return ResCode.raise_success(31221, **r)


@router.post('/{match_id}/tourney',
             summary='把对局添加到比赛，并把成绩按照比赛图池过滤。')
async def match_filter_by_tourney(*,
                                  match_id: int,
                                  tourney_name: str,
                                  background_tasks: BackgroundTasks):
    if crud.matches.get_match(match_id):
        return ResCode.raise_error(32201, match_id=match_id)

    match_data = crud.matches.create_match(match_id)
    if not match_data:
        return ResCode.raise_error(34201, match_id=match_id)

    tourney = crud.tourney.get_tourney(tourney_name)
    if not tourney:
        return ResCode.raise_error(32101, tourney_name=tourney_name)

    match = crud.matches.parse_match(match_id, match_data)
    r = crud.matches.push_match_to_tourney(tourney, match)
    # 没有任何可用图池时，删除比赛。
    if r.get('total_events') == r.get('removed_events'):
        crud.matches.delete_match(match)
        return ResCode.raise_error(32211)

    # 初始化第一次参加比赛的玩家数据，必须初始化后才能计算ELO。
    init_user(match.joined_player)
    # 后台任务刷新所有参赛用户数据。
    background_tasks.add_task(init_user, match.joined_player, refresh=True)

    return ResCode.raise_success(31211, **r)


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
