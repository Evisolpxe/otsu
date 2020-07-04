from mongoengine import *

import datetime


class MappoolMap(DynamicDocument):
    beatmap_id = IntField(required=True, min_value=0)
    mods = ListField(required=True)
    mod_index = IntField(required=True, min_value=1)
    selector = IntField()

    mappool = ReferenceField('Mappool', required=True)
    stage = ReferenceField('MappoolStage', required=True)


class MappoolStage(DynamicDocument):
    mappool = ReferenceField('Mappool', required=True, unique_with='stage')
    maps = ListField(ReferenceField(MappoolMap, reverse_delete_rule=PULL))
    stage = StringField(required=True)
    recommend_elo = ListField(IntField())

    tourneys = ListField(ReferenceField('Tourney'))
    matches = ListField(ReferenceField('Match'))


class MappoolComments(Document):
    user_id = IntField(min_value=0)
    content = StringField()
    reply = StringField(default='')
    timestamp = DateTimeField(default=datetime.datetime.now)

    mappool = ReferenceField('Mappool', required=True)


class MappoolRating(Document):
    mappool = ReferenceField('Mappool', required=True, unique_with='user_id')
    user_id = IntField(min_value=0)
    rating = IntField(min_value=0, max_value=5)


class Mappool(DynamicDocument):
    mappool_name = StringField(required=True, unique=True)
    acronym = StringField(required=True, unique=True)
    host = IntField(required=True)
    cover = IntField(default=0)
    status = StringField(default='Pending', choices=['Pending', 'Ranked', 'Overjoy'])
    description = StringField(max_length=3000, default='主办很懒所以主办什么都不写。')
    recommend_elo = ListField(IntField())

    stages = ListField(ReferenceField(MappoolStage, reverse_delete_rule=PULL))
    comments = ListField(ReferenceField(MappoolComments, reverse_delete_rule=PULL))
    ratings = ListField(ReferenceField(MappoolRating, reverse_delete_rule=PULL))


MappoolStage.register_delete_rule(MappoolMap, 'stage', CASCADE)
Mappool.register_delete_rule(MappoolComments, 'mappool', CASCADE)
Mappool.register_delete_rule(MappoolRating, 'mappool', CASCADE)
Mappool.register_delete_rule(MappoolStage, 'mappool', CASCADE)
