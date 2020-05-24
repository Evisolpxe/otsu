from . import *


class MatchData(DynamicDocument):
    match_id = IntField(required=True)