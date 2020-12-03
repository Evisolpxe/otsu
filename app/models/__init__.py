from mongoengine import connect

from app.models.matches import Match, MatchGame, MatchScore


connect('otsu-v2')

# MatchGame.drop_collection()
# Match.drop_collection()
# Score.drop_collection()

# Match.delete_match(70673286)

