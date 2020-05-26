from mongoengine import *

import datetime


class MappoolDetail(EmbeddedDocument):
    beatmap_id = IntField(required=True, min_value=0)
    index = IntField(required=True, min_value=1)
    selector = IntField(required=True)


class MappoolMod(DynamicEmbeddedDocument):
    pass


class MappoolStage(DynamicDocument):
    mappool = ReferenceField('Mappool')
    stage = StringField(required=True)
    mods = EmbeddedDocumentField(MappoolMod)


class MappoolComments(Document):
    content = StringField()
    user_id = IntField(min_value=0)
    reply = IntField(min_value=0, default=0)
    timestamp = DateTimeField(default=datetime.datetime.now)


class MappoolRating(Document):
    rating = IntField(min_value=0, max_value=5)
    user_id = IntField(min_value=0)


class Mappool(Document):
    mappool_name = StringField(required=True)
    host = IntField(required=True)
    recommend_elo = IntField(min_value=0, max_value=3000)
    cover = IntField()
    status = StringField(default='Pending')

    mappools = ListField(ReferenceField(MappoolStage))
    comments = ListField(ReferenceField(MappoolComments))
    ratings = ListField(ReferenceField(MappoolRating))

#
