from typing import List

from mongoengine.errors import ValidationError
from fastapi import HTTPException, status

from app import models, schemas


def get_all_mappool() -> List[models.Mappool.objects]:
    return models.Mappool.objects().all()


def get_mappool(mappool_name: str) -> models.Mappool.objects:
    return models.Mappool.objects(mappool_name=mappool_name).first()


def calc_rating(rating_list: List[models.MappoolRating]) -> schemas.mappool.MappoolRatingCount:
    if not rating_list:
        return schemas.mappool.MappoolRatingCount(counts=0, avg=0)
    counts = len(rating_list)
    avg = sum([i.rating for i in rating_list]) / counts
    return schemas.mappool.MappoolRatingCount(counts=counts, avg=round(avg, 3))


def create_mappool(t: schemas.mappool.CreateMappool) -> None:
    try:
        mappool = models.Mappool(**dict(t))
        mappool.save()
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=str(e))
