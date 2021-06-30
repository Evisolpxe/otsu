from app.schemas.mongo import MongoModel


class UserEloSchema(MongoModel):
    user_id: int
    current_elo: int
    init_elo: int

class EloChangeSchema(MongoModel):
    match_id: int
    difference: int
