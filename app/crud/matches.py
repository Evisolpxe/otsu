from typing import List
from json.decoder import JSONDecodeError

from app.models.matches import Match, MatchData, EventResult, Score
from app.models.tourney import Tourney
from app.models.mappool import Mappool
from app.api.get import get_match_by_history
from app.core.match_parse import MatchParser


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

    MatchParser(match_id, data)
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
    maps = [beatmap.beatmap_id for mappool in tourney for beatmap in mappool.mappools]
    for event in match:
        if event.beatmap_id not in maps:
            event.delete()
    return tourney.update(push__matches=match)


def push_match_to_mappool(mappool: Mappool, match: Match):
    maps = [beatmap.beatmap_id for beatmap in mappool.mappools]
    for event in match:
        if event.beatmap_id not in maps:
            event.delete()
    return mappool.update(push__matches=match)
