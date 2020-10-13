from enum import Enum
from typing import List
from collections import namedtuple

from ..models import Match

MINIMUM_VALID_MATCH = 5
MINIMUM_PLAYER = 2


class BaseRule:

    def __init__(self, match: Match, warm_up: int = 0, map_pool: List[int] = None):
        """
        :param match: Match Object，包含完整的比赛数据
        :param warm_up: 热手数量，会过滤掉前N场对局
        :param map_pool: 默认为空，过滤掉非比赛地图
        """
        self._validation = True
        self._message = ''
        self._players = {}

        self.match = match
        self.warm_up = warm_up
        self.map_pool = map_pool

        self.valid_game = []
        self.game_filter()

    def game_filter(self) -> Match.games:
        # 滤过热手和非赛图
        self.valid_game = [game for game in self.match.games[self.warm_up:]]
        if self.map_pool:
            self.valid_game = [game for game in self.valid_game if game.beatmap_id in self.map_pool]

    def minimum_games(self) -> None:
        if len(self.match.games) < 5:
            self._validation = False
            self._message = f'有效对局为{len(self.match.games)}局，至少需要5局才可记录成绩。'

    def min_players(self):
        pass


class Solo:

    def __init__(self):
        pass


class StandardElo:
    pass


class PerformanceLibrary(Enum):
    solo = Solo
    elo = StandardElo
