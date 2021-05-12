from __future__ import annotations

import datetime
from math import log
from typing import Optional, List

from mongoengine import (
    DynamicDocument,
    IntField,
    StringField,
    DateTimeField,
    queryset_manager
)
from mongoengine.queryset.visitor import Q


