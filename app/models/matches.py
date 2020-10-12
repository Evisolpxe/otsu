from __future__ import annotations
from typing import Optional

from mongoengine import (
    Document,
    IntField,
    FloatField,
    StringField,
    DateTimeField,
    ListField,
    ReferenceField
)

from ..osu_api import api_v1


class Score(Document):
    user_id = IntField(required=True)
    score = IntField()
    accuracy = FloatField()
    max_combo = IntField()
    count50 = IntField()
    count100 = IntField()
    count300 = IntField()
    count_miss = IntField()
    pass_ = IntField(db_field='pass')
    enable_mods = IntField()
    team = IntField()
    slot = IntField()

    meta = {
        'indexes': ['user_id']
    }


class MatchGame(Document):
    game_id = IntField(required=True, unique=True)
    start_time = DateTimeField()
    end_time = DateTimeField()
    beatmap_id = IntField()
    play_mode = IntField()
    match_type = IntField()
    mods = IntField()
    scores = ListField(ReferenceField(Score))

    meta = {
        'indexes': ['game_id', 'beatmap_id', 'mods']
    }


class Match(Document):
    match_id = IntField(min_value=1, required=True, unique=True)
    name = StringField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    games = ListField(ReferenceField(MatchGame))

    meta = {
        'indexes': ['match_id', 'name']
    }

    @classmethod
    def calc_accuracy(cls, n_300: int, n_100: int, n_50: int, n_0: int) -> float:
        return (50 * n_50 + 100 * n_100 + 300 * n_300) / 300 * (n_300 + n_100 + n_50 + n_0)

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
                games=[
                    MatchGame(
                        game_id=game['game_id'],
                        start_time=game['start_time'],
                        end_time=game['end_time'],
                        beatmap_id=game['beatmap_id'],
                        play_mode=game['play_mode'],
                        match_type=game['match_type'],
                        mods=game['mods'],
                        scores=[
                            Score(
                                user_id=score['user_id'],
                                score=score['score'],
                                max_combo=score['maxcombo'],
                                count50=score['count50'],
                                count100=score['count100'],
                                count300=score['count300'],
                                count_miss=score['countmiss'],
                                pass_=score['pass'],
                                enable_mods=score['enabled_mods'],
                                team=score['team'],
                                slot=score['slot']
                            ).save() for score in game['scores']],
                    ).save() for game in match_data['games']
                ]
            ).save()
