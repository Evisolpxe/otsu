from mongoengine import connect

from .matches import Match, MatchGame, Score
from .users import User

connect('otsu-v2')

MatchGame.drop_collection()
Match.drop_collection()
Score.drop_collection()
Match.get_match(66160343)
# Match.delete_match(66160343)

