from __future__ import annotations

import datetime
from math import log
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

from app.models import users
from global_config import CURRENT_SEASON


class EloFestival(DynamicDocument):
    name = StringField(required=True)
    start_time = DateTimeField(required=True)
    end_time = DateTimeField()
    status = StringField(required=True, choices=['Pending', 'Running', 'Finished'], default='Pending')

    player_list = ListField(IntField())

    def add_festival(self, name: str, start_time: datetime.datetime):
        pass

    def add_player(self, user_list: List[int]):
        return self.modify(player_list__push_all=user_list)

    def set_end_time(self, end_time: datetime.datetime):
        if end_time > self.start_time:
            return self.modify(end_time=end_time)

    @property
    def if_expired(self):
        if datetime.datetime.now() > self.end_time:
            return True


class EloChange(Document):
    match_id = IntField(required=True)
    user_id = IntField(required=True)
    difference = IntField(required=True)
    mode = ReferenceField('EloFestival', reverse_delete_rule=CASCADE)

    @classmethod
    def add_elo_result(cls, match_id: int, elo_change: dict) -> Optional[List[EloChange]]:
        return [cls(match_id=match_id, user_id=user_id, difference=difference).save()
                for user_id, difference in elo_change.items()]

    @classmethod
    def get_elo_result(cls, match_id: int) -> Optional[List[EloChange]]:
        if result := cls.objects(match_id=match_id).all():
            return result

    @classmethod
    def delete_elo_result(cls, match_id: int) -> bool:
        if result := cls.objects(match_id=match_id).all():
            for i in result:
                i.delete()
            return True
        return False

    meta = {
        'indexes': ['match_id', 'user_id']
    }


class UserElo(DynamicDocument):
    user_id = IntField(required=True, unique_with='mode')
    season = StringField()
    init_elo = IntField(required=True)
    mode = ReferenceField('EloFestival', reverse_delete_rule=CASCADE)

    create_time = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'indexes': ['user_id']
    }

    @property
    def current_elo(self):
        return self.init_elo + sum([i.difference for i in self.elo_change_list])

    @property
    def elo_change_list(self):
        return EloChange.objects(user_id=self.user_id, mode=self.mode).order_by('match_id').all()

    @staticmethod
    def _calc_init_elo(rank: int):
        return int(1500 - 600 * log(((int(rank) + 500) / 8500), 4))

    @classmethod
    def get_user_elo(cls, user_id: int) -> UserElo:
        if user := cls.objects(user_id=user_id).first():
            return user
        if user := users.User.get_user(user_id):
            return cls.init_user_elo(user.user_id, user.pp_rank)

    @classmethod
    def init_user_elo(cls, user_id: int, pp_rank: int, mode: str):
        return cls(user_id=user_id, season=CURRENT_SEASON, init_elo=cls._calc_init_elo(pp_rank), mode=mode).save()
