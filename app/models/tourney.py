from mongoengine import *


class Tourney(DynamicDocument):
    tourney_name = StringField(required=True, max_length=50, unique=True)
    chn_name = StringField(max_length=20, unique=True)
    acronym = StringField(max_length=20, unique=True)
    status = StringField()

    elo_coefficient = FloatField(min_value=0, max_value=1, default=1)
    performance_rule = StringField(default='None')
    description = StringField(max_length=3000)
    host = IntField(required=True)
    staffs = ListField(DictField)
    contributor = ListField(IntField)

    matches = ListField(ReferenceField('Match'))
    mappools = ListField(ReferenceField('Mappool'))

    meta = {
        'indexes': ['tourney_name', 'chn_name', 'acronym']
    }


class Quest(DynamicField):
    title = StringField()
    description = StringField()
    rewards = StringField()
    agent = IntField()
