from mongoengine.errors import ValidationError
from fastapi import HTTPException, status

from app import models, schemas


def get_tourney(name: str) -> models.Tourney.objects:
    full = models.Tourney.objects(tourney_name=name).first()
    acronym = models.Tourney.objects(acronym=name).first()
    chn = models.Tourney.objects(chn_name=name).first()

    if full or acronym or chn:
        return full or acronym or chn


def create_tourney(t: schemas.tourney.Tourney) -> None:
    try:
        tourney = models.Tourney(**dict(t))
        tourney.save()
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=str(e))
