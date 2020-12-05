from __future__ import annotations
from math import sqrt

from enum import Enum
from typing import List, Callable, Optional
from operator import itemgetter
from collections import defaultdict

from app.models import Match, MatchResult, GameResult
from app.schemas import GameResultSchema, MatchResultSchema


class BaseRule:

    def __init__(self,
                 match: Match,
                 warm_up: int = 0,
                 map_pool: List[int] = None):
        """
        :param match: Match Object，包含完整的 比赛数据
        :param warm_up: 热手数量，会过滤掉前N场对局
        :param map_pool: 默认为空，过滤掉非比赛地图

        创建新算法需要实现：
        self._calc_game_results() -> List[GameResultSchema]
        其中最重要的是rank_point，最终会统计total_rank_point排名送入算法得到elo变动。
        """
        self._validation = True
        self._message = '解析成功！'

        self.match = match
        self.warm_up = warm_up
        self.map_pool = map_pool

        self.valid_game = self._remove_invalid_game()

        self.game_results: List[GameResultSchema] = []
        self.winner_team = 0
        self.match_winner = []

    def _remove_invalid_game(self) -> Match.games:
        # 滤过少于一人的对局以及热手和非赛图以及未结束的比赛(abort)
        valid_game = [game for game in self.match.games[self.warm_up:] if len(game.scores) >= 2 and game.end_time]
        if self.map_pool:
            valid_game = [game for game in self.valid_game if game.beatmap_id in self.map_pool]
        return valid_game

    def _minimum_games_check(self, times: int) -> None:
        # 最小对局数检测
        if len(self.valid_game) < times:
            self._validation = False
            self._message = f'有效对局为{len(self.match.games)}局，至少需要{times}局才可记录成绩。'

    def _calc_match_result(self) -> None:
        total_rank_point = defaultdict(int)
        win_team_counts = defaultdict(int)
        team_player = defaultdict(set)

        for game in self.game_results:
            # 统计全场rank_point值
            user, rank_point = game.rank_point.popitem()
            total_rank_point[user] += rank_point
            self.performance_rank = {
                user: rank for rank, user in enumerate(
                    sorted(total_rank_point, key=total_rank_point.get, reverse=True), 1)
            }

            # 通过胜场最多的队伍得到胜利队
            win_team_counts[game.winner_team] += 1
            self.winner_team = max(win_team_counts, key=win_team_counts.get)

            # 统计各队玩家
            for team, player in game.player_team.items():
                team_player[team].update(player)
            self.match_winner = list(team_player[self.winner_team]) if self.winner_team \
                else [max(total_rank_point, key=total_rank_point.get)]

    def save_to_db(self):
        if self._validation:
            print([{**dict(i)}
                   for i in self.game_results])
            MatchResult(
                match_id=self.match.match_id,
                winner_team=self.winner_team,
                match_winner=self.match_winner,
                performance_rule=self.__class__.__qualname__,
                performance_rank=self.performance_rank,
                game_results=[GameResult(**dict(i)).save()
                              for i in self.game_results]
            ).save()
        return {'message': self._message, 'validation': self._validation}


class SoloRule(BaseRule):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = 'solo'
        self.description = '比赛为1v1时使用的算法。'

        self._minimum_games_check(4)
        self._calc_game_results()
        self._calc_match_result()

    def _calc_game_results(self) -> None:
        for game in self.valid_game:

            valid_scores = [score for score in game.scores if score.score >= 10000]
            if len(valid_scores) != 2:
                self._validation = False
                self._message = '比赛人数不为2人，无法使用单挑规则哦！'
                break
            sorted_ranking = sorted(game.scores, key=itemgetter('score'))

            self.game_results.append(
                GameResultSchema(
                    game_id=game.game_id,
                    rank_point={sorted_ranking[0].user_id: 1, sorted_ranking[1].user_id: 0},
                    winner_team=0,
                    game_winner=[sorted_ranking[0].user_id],
                    player_team={0: [sorted_ranking[0].user_id, sorted_ranking[1].user_id]}
                )
            )


class HeadToHeadRule(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._minimum_games_check(2)
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


class EloRule(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.win_bonus: float = 0.035
        self.threshold: float = 0.115

        self.name = 'elo'
        self.description = '标准elo算法。'

        self._minimum_games_check(2)

        self.match_point = defaultdict(int)

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

    def calc_rank_point(self, score: int, total_score: int, player_number: int, bonus: float) -> float:
        return round(player_number * sqrt(score) / sqrt(total_score) / 8 - self.threshold + bonus, 4)

    def run(self):
        pass

# class PerformanceLibrary(Enum):
#     solo = SoloRule
#     elo = EloRule
