from __future__ import annotations

from typing import Optional
from datetime import datetime

from mongoengine import (
    DynamicDocument,
    IntField,
    StringField,
    DateTimeField,
    queryset_manager
)
from mongoengine.queryset.visitor import Q

from ..api import api_v1


class User(DynamicDocument):
    user_id = IntField(required=True)
    username = StringField()
    join_date = DateTimeField()
    pp_rank = IntField()
    query_time = DateTimeField(default=datetime.now)

    @queryset_manager
    def objects(self, queryset):
        # 默认取最新数据
        return queryset.order_by('-query_time')

    meta = {
        'indexes': ['user_id', 'username']
    }

    @classmethod
    def get_user(cls, user_id: int = None, username: str = None, renew: bool = False) -> Optional[User]:
        if not (user_id or username):
            return
        if (user := cls.objects(Q(user_id=user_id) | Q(username=username)).first()) and not renew:
            return user
        if user_data := api_v1.get_user(user_id=user_id, username=username):
            return cls(**user_data[0]).save()
