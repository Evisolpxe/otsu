from mongoengine import connect

from .matches import Match

connect('otsu-v2')

from app.osu_api import api_v1

Match(**api_v1.get_match(66160343)).save()
