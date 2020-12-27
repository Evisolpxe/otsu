from mongoengine import connect

from global_config import MONGO_CONNECTION_STRING

connect(host=MONGO_CONNECTION_STRING)


