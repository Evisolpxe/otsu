import datetime
from mongoengine import *


class EloHistory(DynamicDocument):
    user_id = IntField(required=True)
    elo = IntField(required=True)
    season = StringField()
    add_time = DateTimeField(default=datetime.datetime.now)


class Elo(Document):
    user_id = IntField(required=True)
    match_id = IntField(required=True, default=-1)
    elo = IntField(required=True)
    difference = IntField(required=True, default=0)

    match_obj = ReferenceField('Match')


class Users(DynamicDocument):
    user_id = IntField(required=True, primary_key=True)
    raw_data = DynamicField()
    lang = StringField(default='None')

    elo_history = ListField(ReferenceField(EloHistory, reverse_delete_rule=PULL), default=[])
    latest_elo = ReferenceField('Elo', reverse_delete_rule=PULL)
