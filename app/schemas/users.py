import datetime
from typing import List, Set, Dict, Optional

from pydantic import Field
from app.models.mongo import MongoModel, PyObjectId

class UserEloSchema(MongoModel):
    user_id: int
    current_elo: int
    init_elo: int