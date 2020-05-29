from mongoengine.errors import ValidationError
from fastapi import HTTPException, status

from app import schemas
from app.models.tourney import Tourney


def get_tourney(name: str) -> Tourney.objects:
    full = Tourney.objects(tourney_name=name).first()
    acronym = Tourney.objects(acronym=name).first()
    chn = Tourney.objects(chn_name=name).first()

    if full or acronym or chn:
        return full or acronym or chn


def create_tourney(t: schemas.tourney.Tourney) -> None:
    try:
        tourney = Tourney(**dict(t))
        tourney.save()
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=str(e))
