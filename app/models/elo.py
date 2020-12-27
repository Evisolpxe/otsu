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
    CASCADE, Q
)

from app.models import users, matches
from global_config import CURRENT_SEASON


class EloFestival(DynamicDocument):
    name = StringField(required=True, unique=True)
    acronym = StringField(required=True, unique=True)
    start_time = DateTimeField(required=True)
    end_time = DateTimeField()
    status = StringField(required=True, choices=['Pending', 'Opening', 'Running', 'Finished'], default='Pending')

    meta = {
        'indexes': ['name', 'acronym']
    }

    @classmethod
    def add_festival(cls, name: str, acronym: str, start_time: datetime.datetime) -> EloFestival:
        return cls(name=name, acronym=acronym, start_time=start_time).save()

    @classmethod
    def get_festival(cls, name: str) -> EloFestival:
        return cls.objects(Q(name=name) | Q(acronym=name)).first()

    def set_end_time(self, end_time: datetime.datetime):
        if end_time > self.start_time:
            return self.modify(end_time=end_time)

    @property
    def if_expired(self):
        if datetime.datetime.now() > self.end_time:
            return True


class EloChange(Document):
    # 注意：不把change和result绑定，是因为可能会出现比赛以外的elo变动。
    match_id = IntField(required=True)
    user_id = IntField(required=True)
    difference = IntField(required=True)
    elo_festival = ReferenceField('EloFestival', reverse_delete_rule=CASCADE)

    @classmethod
    def add_elo_result(cls, match_id: int, elo_change: dict, elo_festival: EloFestival) -> Optional[List[EloChange]]:
        return [cls(match_id=match_id, user_id=user_id, difference=difference, elo_festival=elo_festival).save()
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
    user_id = IntField(required=True, unique_with='elo_festival')
    season = StringField()
    init_elo = IntField(required=True)
    elo_festival = ReferenceField('EloFestival', reverse_delete_rule=CASCADE)

    create_time = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'indexes': ['user_id']
    }

    @property
    def current_elo(self):
        return self.init_elo + sum([i.difference for i in self.elo_change_list])

    @property
    def elo_change_list(self):
        return EloChange.objects(user_id=self.user_id, elo_festival=self.elo_festival).order_by('match_id').all()

    @staticmethod
    def _calc_init_elo(rank: int):
        return int(1500 - 600 * log(((int(rank) + 500) / 8500), 4))

    @classmethod
    def get_user_elo(cls, user_id: int, elo_festival: str) -> Optional[UserElo]:
        if not (elo_festival := EloFestival.get_festival(elo_festival)):
            return
        if user := cls.objects(user_id=user_id, elo_festival=elo_festival).first():
            return user
        if user := users.User.get_user(user_id):
            return cls.init_user_elo(user.user_id, user.pp_rank, elo_festival)

    @classmethod
    def init_user_elo(cls, user_id: int, pp_rank: int, elo_festival: EloFestival):
        return cls(user_id=user_id, season=CURRENT_SEASON, init_elo=cls._calc_init_elo(pp_rank),
                   elo_festival=elo_festival).save()
