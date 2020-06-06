import json
from typing import List

from pymongo.errors import DuplicateKeyError
from mongoengine.errors import ValidationError, NotUniqueError
from fastapi import HTTPException, status

from app import schemas
from app.crud.maps import get_beatmap
from app.models.mappool import Mappool, MappoolMap, MappoolRating, MappoolComments


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
    t = {k: v for k, v in dict(t).items() if v}
    return q.update(**t)


def delete_mappool(q: Mappool) -> None:
    return q.delete()


# def get_mappool_stage(q: Mappool, t: schemas.mappool.CreateMappoolMaps):
#     return MappoolStage.objects(mappool=q.id, stage=t.stage).first()
#
#
# def update_mappool_stage(q: MappoolStage, t: schemas.mappool.CreateMappoolMaps):
#     maps = [MappoolDetail(**dict(i)) for i in t.maps]
#     return q.update(stage=t.stage, maps=maps)


def get_mappool_maps(q: Mappool) -> List[dict]:

    return [{'object_id': str(i.id),
             'beatmap_id': i.beatmap_id,
             'mod_index': i.mod_index,
             'mods': i.mods,
             'stage': i.stage,
             'selector': i.selector,
             'detail': get_beatmap(i.beatmap_id, mod=i.mods)}
            for i in q.mappools]


def get_mappool_map(q: Mappool, beatmap_id: int) -> MappoolMap:
    return MappoolMap.objects(mappool=q.id, beatmap_id=beatmap_id).first()


def update_mappool_map(beatmap: MappoolMap, t: schemas.mappool.MappoolMap):
    return beatmap.update(**dict(t))


def delete_mappool_map(beatmap: MappoolMap):
    return beatmap.delete()


def get_mappool_map_by_id(object_id: MappoolMap.id):
    return MappoolMap.objects(id=object_id).first()


def create_mappool_map(q: Mappool, t: List[schemas.mappool.MappoolMap]) -> dict:
    try:
        map_list = [i.beatmap_id for i in MappoolMap.objects(beatmap_id__in=[i.beatmap_id for i in t]).all()]
        counts = 0
        for i in t:
            if i.beatmap_id not in map_list:
                beatmap = MappoolMap(mappool=q.id, stage=i.stage, beatmap_id=i.beatmap_id, mods=i.mods,
                                     selector=i.selector, mod_index=i.mod_index)
                beatmap.save()
                push_map_to_mappool(q, beatmap)
                counts += 1
        return {'total_map': len(map_list), 'uploaded': counts, 'mappool_name': q.mappool_name}
    except (DuplicateKeyError, NotUniqueError) as e:
        raise HTTPException(status_code=status.HTTP_200_OK, detail='已有同名stage，请尝试更换或修改操作喔！')
    # except  as e:
    #     print(e)
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='谱面Index似乎重复了，请检查一下喔！')


def push_map_to_mappool(q: Mappool, beatmap: MappoolMap) -> Mappool:
    return q.update(push__mappools=beatmap.id)


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
