from mongoengine import *


class MapData(DynamicDocument):
    beatmap_id = IntField(required=True, unique_with='mod')
    beatmapset_id = IntField()
    mod = IntField()

    meta = {
        'indexes': ['beatmap_id']
    }
