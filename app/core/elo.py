from math import log, sqrt


class EloCalculator:

    def __init__(self, player_scores: dict, player_elo: dict, scoring_type: str, team_type: str):
        self.player_scores = player_scores
        self.player_elo = self.add_virtual_player(player_elo)

        self.scoring_type = scoring_type
        self.team_type = team_type

        self.win_bonus = 0.03
        self.threshold = 0.115

    @staticmethod
    def calc_rank_probability(rival_elo: int, my_elo: int) -> float:
        """Codeforces Rating System 计算期望排名概率"""
        return 1 / (1 + pow(10, (my_elo - rival_elo) / 400))

    @staticmethod
    def calc_rating_change(expect: int, actual: int) -> float:
        return (expect - actual) / 3

    @staticmethod
    def anti_inflate(rating_change: float, inc) -> float:
        return rating_change - sum(inc) / len(inc)

    @staticmethod
    def calc_winner_team(red_score: float, blue_score: float) -> str:
        if red_score > blue_score:
            return 'red'
        elif red_score < blue_score:
            return 'blue'
        else:
            return 'None'

    @staticmethod
    def add_virtual_player(player_elo: dict) -> dict:
        # 虚拟player用于降低elo波动
        sorted_elo_list = sorted([elo for elo in player_elo.values()], reverse=True)
        player_elo['max'] = sorted_elo_list[0] + max(400, sorted_elo_list[0] - sorted_elo_list[1])
        player_elo['min'] = sorted_elo_list[-1] - max(400, sorted_elo_list[0] - sorted_elo_list[1])
        return player_elo

    @staticmethod
    def sorted_rank_point_dict(rank_point_dict) -> dict:
        # 获得玩家最终rank_point的排名。
        return {str(x[0]): i for i, x in enumerate(
            sorted(rank_point_dict.items(), key=lambda x: x[1], reverse=True), 1
        )}

    @staticmethod
    def num_of_player_check(scores: dict) -> bool:
        if len(scores) >= 2:
            return True
        return False

    @staticmethod
    def rank_point_limiter(rank_point):
        if rank_point > 0.08:
            return 0.08
        elif rank_point < -0.03:
            return 0.03
        else:
            return rank_point

    def no_fail_mod_check(self, mods: list, score: int):
        if 'NF' in mods and self.scoring_type == 'score':
            return score * 2
        return score

    def calc_rank_point(self, score: int, total_score: int, player_number: int, bonus: float) -> float:
        return round(player_number * sqrt(score) / total_score / 8 - self.threshold + bonus, 4)

    def calc_rank_point_by_event(self) -> dict:
        rank_point_dict = {}

        for event_id, scores in self.player_scores.items():
            if not self.num_of_player_check(scores):
                continue

            sqrt_sum_score = 0
            team_score = {'red': 0, 'blue': 0}

            for player in scores:
                player_score = self.no_fail_mod_check(player['free_mods'], player['score'])
                if self.scoring_type == 'team-vs':
                    team_score[player['team_color']] += player_score
                sqrt_sum_score += sqrt(player_score)

            winner_team = self.calc_winner_team(team_score.get('red'), team_score.get('blue'))

            for player in scores:
                bonus = self.win_bonus
                player_score = self.no_fail_mod_check(player['free_mods'], player['score'])
                if player['team_color'] != winner_team:
                    bonus = 0
                rank_point = self.calc_rank_point(player_score, sqrt_sum_score, len(scores), bonus)
                rank_point = self.rank_point_limiter(rank_point)

                if player['user_id'] not in rank_point_dict:
                    rank_point_dict[player['user_id']] = {}
                rank_point_dict[player['user_id']][event_id] = rank_point
        return rank_point_dict

    def calc_seed(self, my_id: int, my_elo: int, player_elo: dict) -> float:
        """除自己外所有其他参赛者的成绩都比自己好的概率"""
        seed = 1
        for player_id, elo in player_elo.items():
            if player_id != my_id:
                seed += self.calc_rank_probability(elo, my_elo)
        return seed

    def calc_expect_elo(self, my_id: int, rank: float, player_dict: dict) -> int:
        # 二分法计算期望elo
        left = 1
        right = 8000
        while right - left > 1:
            mid = int((left + right) / 2)
            if self.calc_seed(my_id, mid, player_dict) < rank:
                right = mid
            else:
                left = mid + 1
        return left

    def main(self) -> dict:
        d_i_list, elo_change_dict = [], {}

        total_rank_point = {}
        total_rank_point_by_event = self.calc_rank_point_by_event()

        for user_id, event in self.calc_rank_point_by_event().items():
            total_rank_point[user_id] = 0
            for rank_point in event.values():
                total_rank_point[user_id] += rank_point

        sorted_player_rank = self.sorted_rank_point_dict(total_rank_point)

        for player_id, elo in self.player_elo.items():
            if player_id not in ('min', 'max'):
                seed = self.calc_seed(player_id, elo, self.player_elo)
                m_i = sqrt(seed * (sorted_player_rank[str(player_id)] + 1))
                r_i = self.calc_expect_elo(player_id, m_i, self.player_elo)
                d_i = self.calc_rating_change(r_i, elo)
                d_i_list.append(d_i)
                elo_change_dict[player_id] = d_i

        elo_change_dict = {player: int(self.anti_inflate(change, d_i_list))
                           for player, change in elo_change_dict.items()}

        return {'elo_change_dict': elo_change_dict, 'rank_point': total_rank_point_by_event}
