from mongoengine import *


class Tourney(DynamicDocument):
    tourney_name = StringField(required=True, max_length=50, primary_key=True)
    chn_name = StringField(max_length=20)
    acronym = StringField(max_length=10)
    host = IntField(required=True)
    elo_coefficient = FloatField(min_value=0, max_value=1, default=1)
    description = StringField(max_length=500)
    contributor = ListField(field=IntField)
