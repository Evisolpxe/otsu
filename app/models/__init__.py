from mongoengine import connect

from .matches import Match, MatchGame, Score
from .users import User

connect('otsu-v2')

print(User.get_user(username='Explosive').query_time)