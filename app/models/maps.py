from mongoengine import *


class MapData(DynamicDocument):
    beatmap_id = IntField(required=True)

    meta = {
        'indexes': ['beatmap_id']
    }
