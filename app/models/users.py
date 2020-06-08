from mongoengine import *


class EloHistory(DynamicDocument):
    user_id = IntField(required=True)
    elo = IntField(required=True)
    season = StringField()


class Users(DynamicDocument):
    user_id = IntField(required=True, primary_key=True)
    raw_data = DynamicField()
    lang = StringField(default='None')

    elo_history = ListField(ReferenceField(EloHistory, reverse_delete_rule=PULL))
    season_elo = IntField()
    current_elo = IntField()

    joined_events = ListField(ReferenceField('EventResult'))
