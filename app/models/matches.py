from mongoengine import (
    Document,
    IntField,
    StringField,
    DateTimeField,
    ListField,
    ReferenceField
)


class Score(Document):
    user_id = IntField(required=True)
    score = IntField()


class MatchGame(Document):
    game_id = IntField(required=True, unique=True)
    start_time = DateTimeField()
    end_time = DateTimeField()
    beatmap_id = IntField()
    play_mode = IntField()
    match_type = IntField()
    mods = IntField()
    scores = ListField()


class Match(Document):
    match_id = IntField(min_value=1, required=True, unique=True)
    name = StringField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    games = ListField(ReferenceField(MatchGame))

    meta = {
        'indexes': ['match_id', 'name']
    }
