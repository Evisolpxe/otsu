from mongoengine import connect

from global_config import MONGO_CONNECTION_STRING

connect(db='otsu-v3', host=MONGO_CONNECTION_STRING)


