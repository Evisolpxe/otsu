from collections import defaultdict
from math import sqrt

from app.core.error import ResCode
from app.models.matches import Match, EventResult, Score

from app.core.elo import EloCalculator


class PerformanceAlgo:

    def __init__(self, match: Match):
        self.match = match

    def run(self) -> dict:
        if self.match.tourney.performance_rule:
            if self.match.tourney.performance_rule == 'Tourney':
                return TourneyPerformance(self.match).main()
            elif self.match.tourney.performance_rule == 'Solo':
                return SoloPerformance(self.match).main()
        return {}


class TourneyPerformance:

    def __init__(self, match: Match):
        self.match: Match = match
        self.error_message: dict = {}

        self.win_bonus: float = 0.035
        self.threshold: float = 0.115

        self.match_point: defaultdict = defaultdict(int)

    def main(self):
        for event in self.match.events:
            event: EventResult
            total_score = sum([self.no_fail_mod_checker(player, event.scoring_type)
                               for player in event.scores])

            rank_points = {}
            for player in event.scores:
                player: Score
                bonus = self.win_bonus if player.team == event.win_team else 0
                rank_points[player.user_id] = self.rank_point_limiter(
                    self.calc_rank_point(player.score, total_score, len(event.scores), bonus))

            for user_id, rp in rank_points.items():
                self.match_point[user_id] += rp

            event.rank_point = rank_points
            event.save()

        return EloCalculator(self.sorted_rank_point_dict()).main()

    @staticmethod
    def rank_point_limiter(rank_point):
        if rank_point > 0.08:
            return 0.08
        elif rank_point < -0.03:
            return 0.03
        else:
            return rank_point

    @staticmethod
    def no_fail_mod_checker(score: Score, scoring_type):
        if 'NF' in score.mods and scoring_type == 'score':
            return score.score * 2
        return score.score

    def sorted_rank_point_dict(self) -> dict:
        # 获得玩家最终rank_point的排名。
        return {str(x[0]): i
                for i, x in enumerate(
                sorted(self.match_point.items(), key=lambda x: x[1], reverse=True), 1)
                }

    def calc_rank_point(self, score: int, total_score: int, player_number: int, bonus: float) -> float:
        return round(player_number * sqrt(score) / total_score / 8 - self.threshold + bonus, 4)


class SoloPerformance:

    def __init__(self, match: Match):
        self.match: Match = match
        self.valid_match: bool = True
        self.error_message: dict = {}

        self.win_bonus: float = 1
        self.match_point: defaultdict = defaultdict(int)

    def main(self) -> dict:
        self.round_check()
        for event in self.match.events:
            self.num_of_player_check(event.scores)
            player1, player2 = event.scores[0], event.scores[1]
            if player1.passed and player2.passed:
                if player1.score > player2.score:
                    self.match_point[player1.user_id] += 1
                else:
                    self.match_point[player2.user_id] += 1
            else:
                if player1.passed:
                    self.match_point[player1.user_id] += 1
                elif player2.passed:
                    self.match_point[player2.user_id] += 1

        if self.valid_match:
            return EloCalculator(self.sorted_rank_point_dict()).main()
        return self.error_message

    def round_check(self) -> None:
        """小于四回合不计算成绩"""
        if len(self.match.events) < 4:
            self.valid_match = False
            self.error_message = ResCode.raise_error(33210)

    def num_of_player_check(self, scores: list) -> None:
        if len(scores) != 2:
            self.valid_match = False
            self.error_message = ResCode.raise_error(33211)

    def sorted_rank_point_dict(self) -> dict:
        # 获得玩家最终rank_point的排名。
        return {str(x[0]): i
                for i, x in enumerate(
                sorted(self.match_point.items(), key=lambda x: x[1], reverse=True), 1)
                }


class SimplePerformance:

    def __init__(self, rank_result: dict):
        self.rank_result = rank_result
        self.valid_match: bool = True
        self.error_message: dict = {}

    def main(self):
        return EloCalculator(self.rank_result).main()
