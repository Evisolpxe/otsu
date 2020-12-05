from mongoengine import connect

from app.models.matches import *


connect('otsu-v2')

# MatchGame.drop_collection()
# Match.drop_collection()
# Score.drop_collection()

# Match.delete_match(70673286)

