import datetime

from mongoengine import *


class EwcSeason(Document):
    season_id = IntField(required=True)
    season_name = StringField(required=True)
    end_match = IntField(required=True)
    end_time = DateTimeField(default=datetime.datetime.now)


class EwcRecord(DynamicDocument):
    user_id = IntField(required=True, unique=True)
