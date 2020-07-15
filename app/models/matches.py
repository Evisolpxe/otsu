from mongoengine import *

from .users import Elo
from .mappool import MappoolStage


class MatchData(DynamicDocument):
    match_id = IntField(required=True)

    meta = {
        'indexes': ['match_id']
    }


class Score(Document):
    user_id = IntField(required=True)
    accuracy = FloatField()
    mods = ListField(StringField())
    score = IntField(min_value=0)
    max_combo = IntField(min_value=0)
    slot = IntField()
    team = StringField()
    passed = IntField(max_value=1, min_value=0)

    event = ReferenceField('EventResult')


class Stream(EmbeddedDocument):
    streamer = IntField(required=True)
    link = URLField()


class EventResult(DynamicDocument):
    id = IntField(required=True, primary_key=True)
    mods = ListField(StringField())
    scoring_type = StringField()
    team_type = StringField()
    scores = ListField(ReferenceField(Score, reverse_delete_rule=PULL))
    start_time = DateTimeField()

    win_team = StringField()
    rank_point = DictField()

    beatmap_id = IntField()
    match = ReferenceField('Match')


class Match(DynamicDocument):
    tourney = ReferenceField('Tourney', CASCADE)
    match_id = IntField(required=True, unique=True)
    time = DateTimeField(required=True)

    mappool_stage = ReferenceField('MappoolStage', reverse_delete_rule=CASCADE)

    events = ListField(ReferenceField('EventResult', reverse_delete_rule=PULL))
    elo_change = ListField(ReferenceField('Elo', reverse_delete_rule=PULL))

    joined_player = ListField(IntField(), default=[])
    referee = IntField(default=0)
    stream = EmbeddedDocumentField(Stream)


EventResult.register_delete_rule(Score, 'event', CASCADE)
Match.register_delete_rule(EventResult, 'match', CASCADE)
Match.register_delete_rule(Elo, 'match', CASCADE)
Match.register_delete_rule(MappoolStage, 'matches', PULL)


class Qualifier(DynamicDocument):
    """定级五场才能出分"""
    pass
