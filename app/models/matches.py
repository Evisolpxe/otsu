from __future__ import annotations
from typing import Optional, List

import orjson
from mongoengine import (
    Document,
    IntField,
    FloatField,
    StringField,
    DateTimeField,
    ListField,
    DictField,
    ReferenceField,
    PULL
)

from ..api import api_v1


class Score(Document):
    """
        team: if mode doesn't support teams it is 0, otherwise 1 = blue, 2 = red
        pass: if player failed at the end of the map it is 0, otherwise (pass or revive) it is 1
        perfect: 1 = maximum combo of map reached, 0 otherwise
    """
    user_id = IntField(required=True)
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
        'indexes': ['user_id']
    }

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self.accuracy = self.calc_accuracy()

    # @classmethod
    # def calc_accuracy(cls, n_300: int, n_100: int, n_50: int, n_0: int) -> float:
    #     return (50 * n_50 + 100 * n_100 + 300 * n_300) / 300 * (n_300 + n_100 + n_50 + n_0)

    def calc_accuracy(self) -> float:
        return (50 * self.count50 + 100 * self.count100 + 300 * self.count300) / \
               (300 * (self.count300 + self.count100 + self.count50 + self.count_miss))


class MatchGame(Document):
    """
    standard = 0, taiko = 1, ctb = 2, o!m = 3
    scoring winning condition: score = 0, accuracy = 1, combo = 2, score v2 = 3
    team_type: Head to head = 0, Tag Co-op = 1, Team vs = 2, Tag Team vs = 3
    """
    game_id = IntField(required=True, unique=True)
    start_time = DateTimeField()
    end_time = DateTimeField()
    beatmap_id = IntField()
    play_mode = IntField()
    match_type = IntField()
    scoring_type = IntField()
    team_type = IntField()
    mods = IntField()
    scores = ListField(ReferenceField(Score, reverse_delete_rule=PULL))

    meta = {
        'indexes': ['beatmap_id', 'mods']
    }


class Match(Document):
    match_id = IntField(required=True, unique=True)
    name = StringField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    games: List[MatchGame] = ListField(ReferenceField(MatchGame), reverse_delete_rule=PULL)

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
                    start_time=game['start_time'],
                    end_time=game['end_time'],
                    beatmap_id=game['beatmap_id'],
                    play_mode=game['play_mode'],
                    scoring_type=game['scoring_type'],
                    team_type=game['team_type'],
                    match_type=game['match_type'],
                    mods=game['mods'],
                    scores=[Score(
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
            return match.delete()

    def to_dict(self):
        return {
            'match_id': self.match_id,
            'name': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'games': [{
                'game_id': game.game_id,
                'start_time': game.start_time,
                'end_time': game.end_time,
                'beatmap_id': game.beatmap_id,
                'play_mode': game.play_mode,
                'scoring_type': game.scoring_type,
                'team_type': game.team_type,
                'match_type': game.match_type,
                'mods': game.mods,
                'scores': [{
                    'user_id': score.user_id,
                    'score': score.score,
                    'accuracy': score.accuracy,
                    'max_combo': score.max_combo,
                    'count50': score.count50,
                    'count100': score.count100,
                    'count300': score.count300,
                    'count_miss': score.count_miss,
                    'pass': score.pass_,
                    'enable_mods': score.enable_mods,
                    'team': score.team,
                    'slot': score.slot
                } for score in game.scores
                ]
            } for game in self.games
            ]
        }


class GameResult(Document):
    game_id = ReferenceField(MatchGame)
    public_mod = IntField()
    winner_team = IntField()
    game_winner = ListField(IntField())


class MatchResult(Document):
    match = ReferenceField(Match)
    win_scoring_type = IntField()
    match_winner = ListField(IntField())

    performance_rule = StringField()
    performance_rank = DictField()

    game_results = ListField(ReferenceField(GameResult))

    @classmethod
    def parse_match(cls, match_id: int):
        if match := Match.get_match(match_id):
            pass
