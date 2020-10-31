from __future__ import annotations

from enum import Enum
from typing import List, Callable
from operator import itemgetter
from collections import defaultdict

from ..models import Match


class BaseRule:

    def __init__(self,
                 match: Match,
                 warm_up: int = 0,
                 map_pool: List[int] = None):
        """
        :param match: Match Object，包含完整的 比赛数据
        :param warm_up: 热手数量，会过滤掉前N场对局
        :param map_pool: 默认为空，过滤掉非比赛地图
        """
        self._validation = True
        self._message = ''
        self._players = {}

        self.match = match
        self.warm_up = warm_up
        self.map_pool = map_pool

        self.valid_game = self.remove_invalid_map()

    def remove_invalid_map(self) -> Match.games:
        # 滤过少于一人的对局以及热手和非赛图
        valid_game = [game for game in self.match.games[self.warm_up:] if len(game.scores) >= 2]
        if self.map_pool:
            valid_game = [game for game in self.valid_game if game.beatmap_id in self.map_pool]
        return valid_game

    def minimum_games_check(self, times: int) -> None:
        if len(self.valid_game) < times:
            self._validation = False
            self._message = f'有效对局为{len(self.match.games)}局，至少需要5局才可记录成绩。'


class SoloRule(BaseRule):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.minimum_games_check(4)
        if self._validation:
            self.result = self.run()

    def run(self) -> dict:
        win_count = defaultdict(int)
        for game in self.valid_game:
            if len(game.scores) != 2:
                return {'message': '比赛不满足单挑规定哦。'}
            sorted_ranking = sorted(game.scores, key=itemgetter('score'))
            win_count[sorted_ranking[0].user_id] += 1
            win_count[sorted_ranking[1].user_id] += 0
        return win_count


class HeadToHeadRule(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.minimum_games_check(2)
        if self._validation:
            self.result = self.run()

    def default_player_dict(self):
        return {'total': 0, 'times': 0}

    def run(self) -> list:
        point_counts = defaultdict(self.default_player_dict)
        for game in self.valid_game:
            if len(game.scores) < 2:
                continue
            sorted_ranking = sorted(game.scores, key=itemgetter('score'))
            for i, score in enumerate(sorted_ranking):
                point_counts[score.user_id]['total'] += i
                point_counts[score.user_id]['times'] += 1
        return sorted(point_counts.items(), key=lambda x: x[1]['total'])


print(HeadToHeadRule(Match.get_match(66160343), warm_up=2).result)


class EloRule:
    def __init__(self):
        self.win_bonus: float = 0.035
        self.threshold: float = 0.115

        self.match_point = defaultdict(int)

    def run(self):
        pass

    @staticmethod
    def rank_point_limiter(rank_point):
        if rank_point > 0.08:
            return 0.08
        elif rank_point < -0.03:
            return -0.03
        else:
            return rank_point

    @staticmethod
    def score_v1_no_fail_check(score):
        # 1 == no fail
        if score.enable_mods & 1:
            return score.score * 2


class PerformanceLibrary(Enum):
    solo = SoloRule
    elo = EloRule
