from mongoengine import *


class Users(DynamicDocument):
    user_id = IntField(required=True, primary_key=True)
    raw_data = DynamicField()

    elo_history = DictField()
    season_elo = IntField()
    current_elo = IntField()

    joined_events = ListField(ReferenceField('EventResult'))
