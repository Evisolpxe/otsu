from typing import List

from app.models.matches import Match, MatchData, EventResult
from app.api.get import get_match_by_history
from app.core.match_parse import MatchParser


def get_match(match_id: int) -> Match:
    return Match.objects(match_id=match_id).first()


def create_match(match_id: int) -> Match:
    match_data = MatchData.objects(match_id=match_id).first()
    if not match_data:
        data = get_match_by_history(match_id)
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
    pass


def push_match_to_tourney(tourney, match: Match):
    pass
