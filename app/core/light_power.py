from typing import List
from operator import attrgetter
from itertools import groupby
from collections import defaultdict

from app.models.matches import Match, MatchScore


class LightPower:

    def __init__(self, matches: List[Match]):
        games = sorted([game for match in matches for game in match.games], key=attrgetter('beatmap_id'))

        self.grouped_game = groupby(games, key=attrgetter('beatmap_id'))
        self.light_power_item = defaultdict(list)

        self.run()

        self.light_power = {k: round(sum(v) / len(v), 4) for k, v in self.light_power_item.items()}

    @staticmethod
    def calc_avg_score(scores: List[MatchScore]) -> int:
        if scores:
            return int(sum([score.score for score in scores]) / len(scores))

    def run(self):
        for beatmap_id, games in self.grouped_game:
            scores = [score for game in games for score in game.scores]
            avg_score = self.calc_avg_score(scores)
            for score in scores:
                self.light_power_item[str(score.user_id)].append(round(score.score / avg_score, 5))


# OCLR = [85172398, 84972689, 85044339, 84896923, 85501582, 85439390, 85503945, 85546490, 86302764, 86362224]
#
# C = LightPower([Match.get_match(i) for i in OCLR])
#
# print(C.light_power)
