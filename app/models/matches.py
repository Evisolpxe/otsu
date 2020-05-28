from mongoengine import *

from app.models.mappool import MappoolStage


class EloChange(EmbeddedDocument):
    user_id = IntField(required=True)
    value = IntField(required=True)


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


class Stream(EmbeddedDocument):
    streamer = IntField(required=True)
    link = URLField()


class EventResult(DynamicDocument):
    id = IntField(required=True, primary_key=True)
    mods = ListField(StringField())
    scoring_type = StringField()
    scores = ListField(ReferenceField(Score, reverse_delete_rule=PULL))
    start_time = DateTimeField()

    win_team = StringField()
    rank_point = DictField()

    # beatmap_id = ReferenceField()


class Match(DynamicDocument):
    tourney = ReferenceField('Tourney')
    match_id = IntField(required=True)
    time = DateTimeField(required=True)

    mappool = ReferenceField(MappoolStage)
    removed_events = ListField

    result = ListField(ReferenceField(EventResult, reverse_delete_rule=PULL))
    elo_change = EmbeddedDocumentListField(EloChange)

    joined_player = ListField(IntField)
    referee = IntField()
    stream = EmbeddedDocumentField(Stream)



