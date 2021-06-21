from __future__ import annotations
from typing import Optional, List

from mongoengine import (
    Document,
    DynamicDocument,
    IntField,
    FloatField,
    StringField,
    DateTimeField,
    ListField,
    DictField,
    ReferenceField,
    PULL,
    CASCADE
)

from app.api import api_v1

from app.models.elo import UserElo, EloChange, EloFestival


class MatchScore(Document):
    """
        team: if mode doesn't support teams it is 0, otherwise 1 = blue, 2 = red
        pass: if player failed at the end of the map it is 0, otherwise (pass or revive) it is 1
        perfect: 1 = maximum combo of map reached, 0 otherwise
    """
    user_id = IntField(required=True)
    match_id = IntField()
    game_id = IntField()
    score = IntField()
    accuracy = FloatField()
    max_combo = IntField()
    count50 = IntField()
    count100 = IntField()
    count300 = IntField()
    count_miss = IntField()
    pass_ = IntField(db_field='pass')
    perfect = IntField()
    enable_mods = IntField()
    team = IntField()
    slot = IntField()

    meta = {
        'indexes': ['user_id', 'match_id', 'game_id', 'enable_mods']
    }

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.accuracy = self.calc_accuracy()

    @classmethod
    def delete_score(cls, score_id: str) -> None:
        if score := cls.objects(id=score_id).first():
            score.delete()

    def calc_accuracy(self) -> float:
        return (50 * self.count50 + 100 * self.count100 + 300 * self.count300) / \
               (300 * (self.count300 + self.count100 + self.count50 + self.count_miss))


class MatchGame(Document):
    """
    standard = 0, taiko = 1, ctb = 2, o!m = 3
    scoring winning condition: score = 0, accuracy = 1, combo = 2, score v2 = 3
    team_type: Head to head = 0, Tag Co-op = 1, Team vs = 2, Tag Team vs = 3
    """
    game_id = IntField(primary_key=True)
    match_id = IntField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    beatmap_id = IntField()
    play_mode = IntField()
    match_type = IntField()
    scoring_type = IntField()
    team_type = IntField()
    mods = IntField()
    scores = ListField(ReferenceField(MatchScore, reverse_delete_rule=PULL))

    meta = {
        'indexes': ['beatmap_id', 'mods']
    }

    @classmethod
    def delete_game(cls, game_id: int) -> None:
        if game := cls.objects(game_id=game_id).first():
            for score in game.scores:
                score.delete()
            game.delete()


class Match(Document):
    match_id = IntField(primary_key=True)
    name = StringField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    games: List[MatchGame] = ListField(ReferenceField(MatchGame, reverse_delete_rule=PULL))

    meta = {
        'indexes': ['name']
    }

    @classmethod
    def get_match(cls, match_id: int) -> Optional[Match]:

        if match := cls.objects(match_id=match_id).first():
            return match

        if match_data := api_v1.get_match(match_id):
            return cls(
                match_id=match_data['match']['match_id'],
                name=match_data['match']['name'],
                start_time=match_data['match']['start_time'],
                end_time=match_data['match']['end_time'],
                games=[MatchGame(
                    game_id=game['game_id'],
                    match_id=match_id,
                    start_time=game['start_time'],
                    end_time=game['end_time'],
                    beatmap_id=game['beatmap_id'],
                    play_mode=game['play_mode'],
                    scoring_type=game['scoring_type'],
                    team_type=game['team_type'],
                    match_type=game['match_type'],
                    mods=game['mods'],
                    scores=[MatchScore(
                        match_id=match_id,
                        game_id=game['game_id'],
                        user_id=score['user_id'],
                        score=score['score'],
                        max_combo=score['maxcombo'],
                        count50=score['count50'],
                        count100=score['count100'],
                        count300=score['count300'],
                        count_miss=score['countmiss'],
                        pass_=score['pass'],
                        enable_mods=score['enabled_mods'] or 0,
                        team=score['team'],
                        slot=score['slot']
                    ).save() for score in game['scores']],
                ).save() for game in match_data['games']]
            ).save()

    @classmethod
    def delete_match(cls, match_id: int) -> int:
        if match := cls.objects(match_id=match_id).first():
            if match_result := MatchResult.get_match_result(match_id):
                match_result.delete_elo()
            for game in match.games:
                for score in game.scores:
                    score.delete()
                game.delete()
            return match.delete()


class GameResult(DynamicDocument):
    """
    team: if mode doesn't support teams it is 0, otherwise 1 = blue, 2 = red
    """
    game_id = ReferenceField(MatchGame, reverse_delete_rule=CASCADE)
    winner_team = IntField()
    game_winner = ListField(IntField())
    rank_point = DictField()
    player_team = DictField()


class MatchResult(DynamicDocument):
    match_id = ReferenceField(Match, reverse_delete_rule=CASCADE)
    winner_team = IntField()
    match_winner = ListField(IntField())
    player_list = ListField(IntField())

    performance_rule = StringField()
    performance_rank = DictField()

    game_results = ListField(ReferenceField(GameResult))
    elo_festival = ReferenceField(EloFestival, reverse_delete_rule=CASCADE)

    @classmethod
    def get_match_result(cls, match_id: int) -> MatchResult:
        return cls.objects(match_id=match_id).first()

    @classmethod
    def add_match_result(
            cls,
            match_id: int,
            elo_rule: str,
            elo_festival: EloFestival,
            warm_up: int = 0,
            map_pool: str = None) -> Optional[dict]:
        from app.core import performance

        available_rule = performance.Performance
        if cls.get_match_result(match_id):
            return {'message': '本场比赛已经记录了成绩哦!', 'validation': False}
        # 如获取不到就重新解析
        if match := Match.get_match(match_id):
            # 寻找可用算法
            if not (rule := available_rule.__members__.get(elo_rule)):
                return {'message': '没有找到可用的算法!', 'validation': False}
            # 解析比赛
            rule_instance = rule.value(match=match, warm_up=warm_up, map_pool=map_pool, elo_festival=elo_festival)
            # 失败则停止解析
            return rule_instance.save_to_db()
        return {'message': '没有找到可用对局。', 'validation': False}

    def calc_elo(self):
        from app.models import elo
        from app.core.elo import EloCalculator

        # 获取较晚场次，删除本场后的所有相关场次elo数据
        related_matches_elo_change_after_this = self.get_all_match_involved_users(self.player_list,
                                                                                  self.match_id)
        for match in related_matches_elo_change_after_this:
            match.delete_elo()

        # 计算elo
        elo_result = EloCalculator(
            self.performance_rank,
            {user_id: elo.UserElo.get_user_elo(user_id, self.elo_festival.name).current_elo
             for user_id in self.player_list}
        ).run()

        elo.EloChange.add_elo_result(self.match_id.match_id, elo_result.get('elo_change'), self.elo_festival)

        for match in related_matches_elo_change_after_this:
            match.calc_elo()

        return elo_result

    def delete_elo(self):
        from app.models import elo
        elo.EloChange.delete_elo_result(self.match_id.match_id)

    @classmethod
    def get_all_match_involved_users(
            cls,
            user_id_list: list,
            festival: str,
            current_match_id: int = 0) -> List[MatchResult]:
        return cls.objects(player_list__in=user_id_list, match_id__gt=current_match_id, festival=festival).order_by(
            '+match_id').all()
