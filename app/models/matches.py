from mongoengine import *

from .tourney import Tourney


class MatchData(DynamicDocument):
    match_id = IntField(required=True)

    meta = {
        'indexes': ['match_id']
    }


class Match(DynamicDocument):
    tourney = ReferenceField(Tourney)
    match_id = IntField(required=True)
