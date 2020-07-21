from typing import List

from app.crud.tourney import get_tourney
from app.models.matches import Score, EventResult, Match
from app.models.tourney import Tourney


class TourneyStatistics:

    def __init__(self, tourney: Tourney):
        self.tourney = tourney
        self.matches: List[Match] = self.tourney.matches
        self.events: List[EventResult] = [e for i in self.matches for e in i.events]
        self.scores: List[Score] = [s for i in self.events for s in i.scores]

    def total_damage(self):
        event_id_list = [i.id for i in self.events]

        a = Score.objects(event_id__in=event_id_list).group_by('user_id').sum('score')
        print(a)


t = get_tourney('oclr_s4')
A = TourneyStatistics(t)

A.total_damage()
