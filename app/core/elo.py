from math import sqrt


class EloCalculator:

    def __init__(self, rank_dict: dict, player_elo: dict):
        self.rank_dict = rank_dict
        self.player_elo = player_elo
        self.init_player_elo = player_elo.copy()
        self._add_virtual_player()

    @staticmethod
    def _calc_rank_probability(rival_elo: int, my_elo: int) -> float:
        """Codeforces Rating System 计算期望排名概率"""
        return 1 / (1 + pow(10, (my_elo - rival_elo) / 400))

    @staticmethod
    def _calc_rating_change(expect: int, actual: int) -> float:
        return (expect - actual) / 3

    @staticmethod
    def _anti_inflate(rating_change: float, inc) -> float:
        return rating_change - sum(inc) / len(inc)

    def _calc_seed(self, my_id: int, my_elo: int, player_elo: dict) -> float:
        """除自己外所有其他参赛者的成绩都比自己好的概率"""
        seed = 1
        for player_id, elo in player_elo.items():
            if player_id != my_id:
                seed += self._calc_rank_probability(elo, my_elo)
        return seed

    def _calc_expect_elo(self, my_id: int, rank: float, player_dict: dict) -> int:
        # 二分法计算期望elo
        left = 1
        right = 8000
        while right - left > 1:
            mid = int((left + right) / 2)
            if self._calc_seed(my_id, mid, player_dict) < rank:
                right = mid
            else:
                left = mid + 1
        return left

    def _add_virtual_player(self) -> None:
        # 虚拟player用于降低elo波动
        sorted_elo_list = sorted([elo for elo in self.player_elo.values()], reverse=True)
        self.player_elo['max'] = sorted_elo_list[0] + max(400, sorted_elo_list[0] - sorted_elo_list[1])
        self.player_elo['min'] = sorted_elo_list[-1] - max(400, sorted_elo_list[0] - sorted_elo_list[1])

    def run(self) -> dict:
        d_i_list, elo_change_dict = [], {}
        for player_id, elo in self.player_elo.items():
            if player_id not in ('min', 'max'):
                seed = self._calc_seed(player_id, elo, self.player_elo)
                m_i = sqrt(seed * (self.rank_dict[str(player_id)] + 1))
                r_i = self._calc_expect_elo(player_id, m_i, self.player_elo)
                d_i = self._calc_rating_change(r_i, elo)
                d_i_list.append(d_i)
                elo_change_dict[player_id] = d_i

        elo_change_dict = {player: int(self._anti_inflate(change, d_i_list))
                           for player, change in elo_change_dict.items()}
        print(self.init_player_elo)
        return {'elo_change': elo_change_dict,
                'player_elo': {user_id: elo + elo_change_dict[user_id] for user_id, elo in self.init_player_elo.items()}}
