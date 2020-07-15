from mongoengine.errors import ValidationError
from fastapi import HTTPException, status

from app import schemas
from app.crud.mappool import acronym_filter
from app.models.tourney import Tourney
from app.models.mappool import MappoolStage


def get_tourney(name: str) -> Tourney:
    return Tourney.objects(tourney_name=name).first() or \
           Tourney.objects(acronym=name).first() or \
           Tourney.objects(chn_name=name).first()


def create_tourney(t: schemas.tourney.Tourney) -> None:
    try:
        t.acronym = acronym_filter(t.acronym)
        tourney = Tourney(**dict(t))
        tourney.save()
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=str(e))


def get_tourney_mappool(tourney: Tourney) -> dict:
    return {stage.stage: [beatmap.beatmap_id for beatmap in stage.maps] for stage in tourney.mappool_stages}


def add_mappool_stage_to_tourney(tourney: Tourney, mappool_stage: MappoolStage):
    return tourney.update(push__mappool_stages=mappool_stage)
