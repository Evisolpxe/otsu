import json
from typing import List

from pymongo.errors import DuplicateKeyError
from mongoengine.errors import ValidationError, NotUniqueError
from fastapi import HTTPException, status

from app import schemas
from app.models.mappool import Mappool, MappoolStage, MappoolRating, MappoolComments, MappoolDetail


def get_all_mappool() -> List[Mappool.objects]:
    return Mappool.objects().all()


def get_mappool(mappool_name: str) -> Mappool.objects:
    return Mappool.objects(mappool_name=mappool_name).first()


def calc_ratings(rating_list: List[MappoolRating]) -> schemas.mappool.MappoolRating:
    if not rating_list:
        return schemas.mappool.MappoolRating(counts=0, avg=0, user_id=[])
    try:
        counts = len(rating_list)
        avg = sum([i.rating for i in rating_list]) / counts
        user_id = [i.user_id for i in rating_list]
    except AttributeError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='啊...溢出了...')
    return schemas.mappool.MappoolRating(counts=counts, avg=round(avg, 3), user_id=user_id)


def create_mappool(t: schemas.mappool.CreateMappool) -> Mappool:
    try:
        mappool = Mappool(**dict(t))
        mappool.save()
        return mappool
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=str(e))


def update_mappool(q: Mappool, t: schemas.mappool.UpdateMappool) -> Mappool:
    return q.update(**dict(t))


def get_mappool_stage(q: Mappool, t: schemas.mappool.CreateMappoolMaps):
    return MappoolStage.objects(mappool=q.id, stage=t.stage).first()


def update_mappool_stage(q: MappoolStage, t: schemas.mappool.CreateMappoolMaps):
    maps = [MappoolDetail(**dict(i)) for i in t.maps]
    return q.update(stage=t.stage, maps=maps)


def get_mappool_map(q: Mappool) -> List[schemas.mappool.CreateMappoolMaps]:
    return [json.loads(i.to_json()) for i in q.mappools]


def create_mappool_map(q: Mappool, t: schemas.mappool.CreateMappoolMaps) -> MappoolStage:
    try:
        maps = [MappoolDetail(**dict(i)) for i in t.maps]
        stage = MappoolStage(mappool=q.id, stage=t.stage, maps=maps)
        stage.save()
        return stage
    except (DuplicateKeyError, NotUniqueError) as e:
        raise HTTPException(status_code=status.HTTP_200_OK, detail='已有同名stage，请尝试更换或修改操作喔！')
    # except  as e:
    #     print(e)
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='谱面Index似乎重复了，请检查一下喔！')


def push_stage_to_mappool(q: Mappool, stage: MappoolStage) -> Mappool:
    return q.update(push__mappools=stage.id)


def get_mappool_rating(q: Mappool) -> schemas.mappool.MappoolRating:
    return calc_ratings(q.ratings)


def get_mappool_rating_by_user(q: Mappool,
                               user_id: int) -> schemas.mappool.MappoolRating:
    return MappoolRating.objects(mappool=q.id, user_id=user_id).first()


def create_mappool_rating(q: Mappool, t: schemas.mappool.CreateMappoolRating) -> MappoolRating:
    rating_value = t.rating
    if q.status == 'Pending' and rating_value < 5:
        rating_value = 1
    rating = MappoolRating(mappool=q.id, user_id=t.user_id, rating=rating_value)
    rating.save()
    return rating


def delete_mappool_rating(q: Mappool, user_id: int):
    return MappoolRating.objects(mappool=q.id, user_id=user_id).delete()


def push_rating_to_mappool(q: Mappool, rating: MappoolRating) -> Mappool:
    return q.update(push__ratings=rating.id)


def get_mappool_comments(q: Mappool) -> List[dict]:
    return [{'comment_id': str(i.id),
             'content': i.content,
             'user_id': i.user_id,
             'timestamp': str(i.timestamp),
             'reply': i.reply}
            for i in q.comments]


def create_mappool_comment(t: schemas.mappool.MappoolComment) -> MappoolComments:
    comment = MappoolComments(**dict(t))
    comment.save()
    return comment


def delete_mappool_comment(comment_id: str):
    return MappoolComments.objects(id=comment_id).delete()


def push_comment_to_mappool(q: Mappool, comment: MappoolComments) -> Mappool:
    return q.update(push__comments=comment.id)
