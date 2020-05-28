import json
from typing import List

from pymongo.errors import DuplicateKeyError
from mongoengine.errors import ValidationError, NotUniqueError
from fastapi import HTTPException, status

from app import models, schemas


def get_all_mappool() -> List[models.Mappool.objects]:
    return models.Mappool.objects().all()


def get_mappool(mappool_name: str) -> models.Mappool.objects:
    return models.Mappool.objects(mappool_name=mappool_name).first()


def calc_ratings(rating_list: List[models.MappoolRating]) -> schemas.mappool.MappoolRating:
    if not rating_list:
        return schemas.mappool.MappoolRating(counts=0, avg=0, user_id=[])
    try:
        counts = len(rating_list)
        avg = sum([i.rating for i in rating_list]) / counts
        user_id = [i.user_id for i in rating_list]
    except AttributeError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='啊...溢出了...')
    return schemas.mappool.MappoolRating(counts=counts, avg=round(avg, 3), user_id=user_id)


def create_mappool(t: schemas.mappool.CreateMappool) -> models.Mappool:
    try:
        mappool = models.Mappool(**dict(t))
        mappool.save()
        return mappool
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=str(e))


def update_mappool(q: models.Mappool, t: schemas.mappool.UpdateMappool) -> models.Mappool:
    return q.update(**dict(t))


def get_mappool_stage(q: models.Mappool, t: schemas.mappool.CreateMappoolMaps):
    return models.MappoolStage.objects(mappool=q.id, stage=t.stage).first()


def update_mappool_stage(q: models.MappoolStage, t: schemas.mappool.CreateMappoolMaps):
    mods = {k: [dict(i) for i in v] for k, v in t.mods.items()}
    return q.update(stage=t.stage, mods=mods)


def get_mappool_map(q: models.Mappool) -> List[schemas.mappool.CreateMappoolMaps]:
    return [json.loads(i.to_json()) for i in q.mappools]


def create_mappool_map(q: models.Mappool, t: schemas.mappool.CreateMappoolMaps) -> models.MappoolStage:
    try:
        mods = {k: [dict(i) for i in v] for k, v in t.mods.items()}
        stage = models.MappoolStage(mappool=q.id, stage=t.stage, mods=mods)
        stage.save()
        return stage
    except (DuplicateKeyError, NotUniqueError) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='已有同名stage，请尝试更换或修改操作喔！')
    # except  as e:
    #     print(e)
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='谱面Index似乎重复了，请检查一下喔！')


def push_stage_to_mappool(q: models.Mappool, stage: models.MappoolStage) -> models.Mappool:
    return q.update(push__mappools=stage.id)


def get_mappool_rating(q: models.Mappool) -> schemas.mappool.MappoolRating:
    return calc_ratings(q.ratings)


def get_mappool_rating_by_user(q: models.Mappool,
                               user_id: int) -> schemas.mappool.MappoolRating:
    return models.MappoolRating.objects(mappool=q.id, user_id=user_id).first()


def create_mappool_rating(q: models.Mappool, t: schemas.mappool.CreateMappoolRating) -> models.MappoolRating:
    rating_value = t.rating
    if q.status == 'Pending' and rating_value < 5:
        rating_value = 1
    rating = models.MappoolRating(mappool=q.id, user_id=t.user_id, rating=rating_value)
    rating.save()
    return rating


def delete_mappool_rating(q: models.Mappool, user_id: int):
    return models.MappoolRating.objects(mappool=q.id, user_id=user_id).delete()


def push_rating_to_mappool(q: models.Mappool, rating: models.MappoolRating) -> models.Mappool:
    return q.update(push__ratings=rating.id)


def get_mappool_comments(q: models.Mappool) -> List[dict]:
    return [{'comment_id': str(i.id),
             'content': i.content,
             'user_id': i.user_id,
             'timestamp': str(i.timestamp),
             'reply': i.reply}
            for i in q.comments]


def create_mappool_comment(t: schemas.mappool.MappoolComment) -> models.MappoolComments:
    comment = models.MappoolComments(**dict(t))
    comment.save()
    return comment


def delete_mappool_comment(comment_id: str):
    return models.MappoolComments.objects(id=comment_id).delete()


def push_comment_to_mappool(q: models.Mappool, comment: models.MappoolComments) -> models.Mappool:
    return q.update(push__comments=comment.id)
