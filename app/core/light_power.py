from typing import List
from operator import attrgetter
from itertools import groupby

from app.models.matches import Match, MatchScore


class LightPower:

    def __init__(self, matches: List[Match]):
        self.grouped_game = groupby([game for match in matches for game in match.games], key=attrgetter('beatmap_id'))

    def calc_avg_score(self, scores: List[MatchScore]):
        pass