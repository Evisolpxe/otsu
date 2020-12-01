from .matches import *


class PublicResponseSchema(BaseModel):
    message: str
    status: str
    code: int
