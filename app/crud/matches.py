from typing import List
from json.decoder import JSONDecodeError

from app import crud
from app.models.matches import Match, MatchData, EventResult, Score
from app.models.tourney import Tourney
from app.models.users import Elo
from app.models.mappool import Mappool, MappoolStage
from app.api.get import get_match_by_history
from app.core.match_parse import MatchParser
from app.core.performance import PerformanceAlgo


def get_match(match_id: int) -> Match:
    return Match.objects(match_id=match_id).first()


def create_match(match_id: int) -> Match or None:
    match_data = MatchData.objects(match_id=match_id).first()
    if not match_data:
        try:
            data = get_match_by_history(match_id)
        except JSONDecodeError:
            return
        match = MatchData(match_id=match_id, data=data)
        match.save()
    else:
        data = match_data.data
    return data


def parse_match(match_id: int, match_data: dict) -> Match:
    MatchParser(match_id, match_data)
    return Match.objects(match_id=match_id).first()


def delete_match(match: Match):
    return match.delete()


def get_event(event_id: int):
    return EventResult.objects(id=event_id).first()


def delete_event(event: EventResult):
    return event.delete()


def get_score(score_id: str):
    return Score.objects(score_id=score_id).first()


def delete_score(score: Score):
    return score.delete()


def push_match_to_tourney(tourney: Tourney, match: Match):
    # Tourney的mappool_stages存的是stage
    maps = [beatmap.beatmap_id for mappool in tourney.mappool_stages for beatmap in mappool.maps]
    counts = 0
    for event in match.events:
        if event.beatmap_id not in maps:
            event.delete()
            counts += 1
    match.update(tourney=tourney)
    tourney.update(push__matches=match)
    return {'total_events': len(match.events), 'total_maps': len(maps), 'removed_events': counts}


def push_match_to_mappool(mappool_stage: MappoolStage, match: Match):
    # 检测图池stage的谱面
    maps = [beatmap.beatmap_id for beatmap in mappool_stage.maps]
    counts: int = 0
    for event in match.events:
        if event.beatmap_id not in maps:
            event.delete()
            counts += 1
    match.update(mappool_stage=mappool_stage)
    mappool_stage.update(push__matches=match)
    return {'total_events': len(match.events), 'total_maps': len(maps), 'removed_events': counts}


def calc_elo(match: Match):
    if not match.tourney:
        return
    result = PerformanceAlgo(match).run()
    elo_coefficient = match.tourney.elo_coefficient
    for user_id, elo_change in result.get('elo_change').items():
        final_elo_change = int(elo_change * elo_coefficient)
        elo = Elo(user_id=user_id,
                  difference=final_elo_change,
                  elo=result['player_elo'][user_id] + final_elo_change,
                  match_id=match.match_id,
                  match=match)
        elo.save()
        match.update(push__elo_change=elo)
        user = crud.users.get_user(user_id)
        user.update(push__elo=elo)
    return True


def calc_all_elo(break_point_match: int) -> int:
    """
    如果break_point为0，意味全部重新计算当前赛季的ELO，否则只会计算match_id之后的elo变化
    """
    # 先删除break_point之后的所有Elo变动
    if break_point_match < 0:
        break_point_match = 0
    Elo.objects(match_id__gte=break_point_match).delete()
    # 获取break_point之后的所有比赛重新计算elo
    matches = Match.objects(match_id__gte=break_point_match, tourney__exists=True, events__size__ne=0).all()
    counts = 0
    for match in matches:
        if calc_elo(match):
            counts += 1
    # 返回计算比赛的个数
    return counts
