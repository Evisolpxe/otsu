from mongoengine import *


class Tourney(DynamicDocument):
    tourney_name = StringField(required=True, max_length=50, unique=True)
    chn_name = StringField(max_length=20, unique=True)
    acronym = StringField(max_length=20, unique=True)
    host = IntField(required=True)
    elo_coefficient = FloatField(min_value=0, max_value=1, default=1)
    description = StringField(max_length=3000)
    staffs = ListField(IntField)
    contributor = ListField(IntField)

    meta = {
        'indexes': ['tourney_name', 'chn_name', 'acronym']
    }
