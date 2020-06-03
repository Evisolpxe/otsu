from mongoengine import *

import datetime


class MappoolMap(DynamicDocument):
    mappool = ReferenceField('Mappool', required=True, unique_with='stage')
    stage = StringField(required=True)
    mods = ListField(required=True)
    beatmap_id = IntField(required=True, min_value=0)
    mod_index = IntField(required=True, min_value=1)
    selector = IntField()

# class MappoolDetail(DynamicEmbeddedDocument):
#     beatmap_id = IntField(required=True, min_value=0)
#     mod_index = IntField(required=True, min_value=1)
#     selector = IntField()


# class MappoolStage(DynamicDocument):
#     mappool = ReferenceField('Mappool', required=True, unique_with='stage')
#     stage = StringField(required=True)
#     mods = DynamicField(required=True)


class MappoolComments(Document):
    user_id = IntField(min_value=0)
    content = StringField()
    reply = StringField(default='')
    timestamp = DateTimeField(default=datetime.datetime.now)


class MappoolRating(Document):
    mappool = ReferenceField('Mappool', required=True, unique_with='user_id')
    user_id = IntField(min_value=0)
    rating = IntField(min_value=0, max_value=5)


class Mappool(Document):
    mappool_name = StringField(required=True, unique=True)
    host = IntField(required=True)
    recommend_elo = IntField(min_value=0, max_value=3000)
    cover = IntField()
    status = StringField(default='Pending')
    description = StringField(max_length=3000)

    mappools = ListField(ReferenceField(MappoolMap, reverse_delete_rule=PULL))
    comments = ListField(ReferenceField(MappoolComments, reverse_delete_rule=PULL))
    ratings = ListField(ReferenceField(MappoolRating, reverse_delete_rule=PULL))
