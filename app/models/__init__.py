from mongoengine import *

from .matches import *
from .maps import *
from .mappool import *
from .tourney import *

connect('otsu')
