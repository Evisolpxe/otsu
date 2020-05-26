from mongoengine import *

from .mappool import *
from .maps import *
from .matches import *
from .tourney import *

connect('otsu')
