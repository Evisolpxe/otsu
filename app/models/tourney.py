from mongoengine import *

from .mappool import MappoolStage


class Tourney(DynamicDocument):
    tourney_name = StringField(required=True, max_length=50, unique=True)
    chn_name = StringField(max_length=20, unique=True)
    acronym = StringField(max_length=20, unique=True)
    status = StringField()

    elo_coefficient = FloatField(min_value=0, max_value=1, default=1)
    performance_rule = StringField(default='Tourney')
    description = StringField(max_length=3000)
    host = IntField(required=True)
    staffs = ListField(DictField)
    contributor = ListField(IntField)

    matches = ListField(ReferenceField('Match', reverse_delete_rule=PULL))
    mappool_stages = ListField(ReferenceField('MappoolStage', reverse_delete_rule=PULL))

    meta = {
        'indexes': ['tourney_name', 'chn_name', 'acronym']
    }


Tourney.register_delete_rule(MappoolStage, 'tourneys', PULL)


class Quest(DynamicField):
    title = StringField()
    description = StringField()
    rewards = StringField()
    agent = IntField()
