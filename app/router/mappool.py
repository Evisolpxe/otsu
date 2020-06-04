import json
from typing import List

from fastapi import APIRouter, status, Query, Path, HTTPException, Response

from app import crud, schemas
from app.models.mappool import MappoolComments
from app.core.error import ResCode

router = APIRouter()


@router.get('/',
            summary='获取全部图池概况，可分页。',
            status_code=status.HTTP_200_OK,
            response_model=List[schemas.mappool.MappoolOverview])
async def get_all_mappool(*,
                          pagination: bool = False, page: int = 0, per_page: int = 30
                          ) -> List[schemas.mappool.MappoolOverview]:
    q_list = crud.mappool.get_all_mappool()
    if not q_list:
        # return ResCode.raise_error(32311)
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='还没有任何图池QwQ...快快上传吧!')

    if pagination:
        start = page * per_page
        end = start + per_page
        q_list = q_list[start: end]

    q_overview = []
    for q in q_list:
        overview = json.loads(q.to_json())
        overview.update({'rating': crud.mappool.calc_ratings(q.ratings)})
        q_overview.append(overview)
    return q_overview


@router.post('/',
             summary='创建新图池。',
             status_code=status.HTTP_201_CREATED)
async def create_mappool(*,
                         t: schemas.mappool.CreateMappool
                         ) -> schemas.RaiseInfo:
    q = crud.mappool.get_mappool(t.mappool_name)
    if q:
        return ResCode.raise_error(12301, mappool_name=t.mappool_name)
    crud.mappool.create_mappool(t)
    return ResCode.raise_success(11301, mappool_name=t.mappool_name)


@router.get('/{mappool_name}',
            summary='获取图池信息。',
            status_code=status.HTTP_200_OK,
            response_model=schemas.mappool.MappoolOverview,
            response_model_exclude_unset=True,
            )
async def get_mappool(*,
                      mappool_name: str = Path(..., description='图池名称，只支持全称查询。')
                      ) -> schemas.mappool.MappoolOverview:
    q = crud.mappool.get_mappool(mappool_name)
    if not q:
        # return ResCode.raise_error(32301, mappool_name=mappool_name)
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='没有找到对应图池哦！')
    overview = json.loads(q.to_json())
    overview.update({'rating': crud.mappool.calc_ratings(q.ratings)})
    return overview


@router.put('/{mappool_name}',
            summary='修改图池信息。',
            status_code=status.HTTP_202_ACCEPTED,
            )
async def update_mappool(*,
                         mappool_name: str = Path(..., description='图池名称，只支持全称查询。'),
                         t: schemas.mappool.UpdateMappool
                         ) -> schemas.RaiseInfo:
    q = crud.mappool.get_mappool(mappool_name)
    if not q:
        return ResCode.raise_error(32301, mappool_name=mappool_name)
    crud.mappool.update_mappool(q, t)
    return ResCode.raise_success(21301, mappool_name=mappool_name)


@router.delete('/{mappool_name}',
               summary='删除图池。')
async def delete_mappool(*,
                         mappool_name: str = Path(..., description='图池名称，只支持全称查询。')
                         ) -> schemas.RaiseInfo:
    q = crud.mappool.get_mappool(mappool_name)
    if not q:
        return ResCode.raise_error(32301, mappool_name=mappool_name)
    crud.mappool.delete_mappool(q)
    return ResCode.raise_success(41301, mappool_name=mappool_name)


@router.get('/{mappool_name}/maps',
            summary='获取图池谱面。',
            status_code=status.HTTP_200_OK,
            response_model=List[schemas.mappool.MappoolMapOut],
            response_model_exclude_unset=True)
async def get_mappool_maps(*,
                           mappool_name: str = Path(..., description='图池名称，只支持全称查询。'),
                           ) -> List[dict]:
    q = crud.mappool.get_mappool(mappool_name)
    if not q:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='没有找到对应图池哦！')
        # return ResCode.raise_error(32301, mappool_name=mappool_name)
    maps = crud.mappool.get_mappool_maps(q)
    # if not maps:
    #     raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='图池里还没有谱面哦！')
    #     # return ResCode.raise_error(32302, mappool_name=mappool_name)
    return maps


@router.post('/{mappool_name}/maps',
             summary='上传图池谱面。',
             status_code=status.HTTP_201_CREATED
             )
async def create_mappool_maps(*,
                              mappool_name: str = Path(..., description='图池名称，只支持全称查询。'),
                              t: List[schemas.mappool.MappoolMap]
                              ) -> schemas.RaiseInfo:
    q = crud.mappool.get_mappool(mappool_name)
    if not q:
        return ResCode.raise_error(32301, mappool_name=mappool_name)
    crud.mappool.create_mappool_map(q, t)
    return ResCode.raise_success(11302, mappool_name=mappool_name)


@router.delete('/{mappool_name}/maps',
               summary='用id修改图池谱面。', )
async def delete_mappool_map_by_id(*,
                                   object_id: str = Query(..., description='object_id'),
                                   t: schemas.mappool.MappoolMap):
    beatmap = crud.mappool.get_mappool_map_by_id(object_id)
    if not beatmap:
        return ResCode.raise_error(32312, object_id=object_id)
    crud.mappool.update_mappool_map(beatmap, t)
    return ResCode.raise_success(21302)


@router.delete('/{mappool_name}/maps',
               summary='用id删除图池谱面。', )
async def delete_mappool_map_by_id(*, object_id: str = Query(..., description='object_id')):
    beatmap = crud.mappool.get_mappool_map_by_id(object_id)
    if not beatmap:
        return ResCode.raise_error(32312, object_id=object_id)
    beatmap.delete()
    return ResCode.raise_success(41302)


@router.get('/{mappool_name}/maps/{beatmap_id}',
            summary='获取这张谱面信息。')
async def get_mappool_map(*,
                          mappool_name: str = Path(..., description='图池名称，只支持全称查询。'),
                          beatmap_id: int = Path(..., description='beatmap_id')
                          ):
    q = crud.mappool.get_mappool(mappool_name)
    if not q:
        return ResCode.raise_error(32301, mappool_name=mappool_name)
    beatmap = crud.mappool.get_mappool_map(q, beatmap_id)
    if not beatmap:
        return ResCode.raise_error(32301, mappool_name=mappool_name)
    return {'object_id': str(beatmap.id),
            'beatmap_id': beatmap.beatmap_id,
            'mod_index': beatmap.mod_index,
            'mods': beatmap.mods,
            'stage': beatmap.stage,
            'selector': beatmap.selector}


@router.put('/{mappool_name}/maps/{beatmap_id}',
            summary='修改图池谱面。',
            status_code=status.HTTP_202_ACCEPTED)
async def update_mappool_map(*,
                             mappool_name: str = Path(..., description='图池名称，只支持全称查询。'),
                             beatmap_id: int = Path(..., description='beatmap_id'),
                             t: schemas.mappool.MappoolMap) -> schemas.RaiseInfo:
    q = crud.mappool.get_mappool(mappool_name)
    if not q:
        return ResCode.raise_error(32301, mappool_name=mappool_name)
    beatmap = crud.mappool.get_mappool_map(q, beatmap_id)
    if not beatmap:
        return ResCode.raise_error(32301, mappool_name=mappool_name)
    crud.mappool.update_mappool_map(beatmap, t)
    return ResCode.raise_success(21302, mappool_name=mappool_name)


@router.delete('/{mappool_name}/maps/{beatmap_id}',
               summary='删除图池谱面。')
async def delete_mappool_map(*,
                             mappool_name: str = Path(..., description='图池名称，只支持全称查询。'),
                             beatmap_id: int = Path(..., description='beatmap_id')
                             ):
    q = crud.mappool.get_mappool(mappool_name)
    if not q:
        return ResCode.raise_error(32301, mappool_name=mappool_name)
    beatmap = crud.mappool.get_mappool_map(q, beatmap_id)
    crud.mappool.delete_mappool_map(beatmap)
    return ResCode.raise_success(41302, mappool_name=mappool_name, beatmap_id=beatmap_id)


@router.get('/{mappool_name}/rating',
            summary='获取图池评价平均星数、评价人数、用户列表。',
            response_model=schemas.mappool.MappoolRating)
async def get_mappool_rating(*,
                             mappool_name: str = Path(..., description='图池名称，只支持全称查询。'),
                             ):
    q = crud.mappool.get_mappool(mappool_name)
    if not q:
        # return ResCode.raise_error(32301, mappool_name=mappool_name)
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='没有找到对应图池哦！')
    return crud.mappool.calc_ratings(q.ratings)


@router.post('/{mappool_name}/rating',
             summary='上传图池评价的星数，⭐1-5，在图池为Pending状态的时候，低于5分的评价全部变成1分。',
             status_code=status.HTTP_201_CREATED)
async def create_mappool_rating(*,
                                mappool_name: str = Path(..., description='图池名称，只支持全称查询。'),
                                t: schemas.mappool.CreateMappoolRating,
                                response: Response
                                ):
    q = crud.mappool.get_mappool(mappool_name)
    if not q:
        return ResCode.raise_error(32301, mappool_name=mappool_name)
    rating = crud.mappool.get_mappool_rating_by_user(q, t.user_id)
    if rating:
        response.status_code = status.HTTP_409_CONFLICT
        return ResCode.raise_error(12303, mappool_name=mappool_name)

    rating = crud.mappool.create_mappool_rating(q, t)
    crud.mappool.push_rating_to_mappool(q, rating)
    return ResCode.raise_success(11303, mappool_name=mappool_name)


@router.delete('/{mappool_name}/rating',
               summary='删除用户的评价!',
               status_code=status.HTTP_202_ACCEPTED)
async def delete_mappool_rating(*,
                                mappool_name: str = Path(..., description='图池名称，只支持全称查询。'),
                                user_id: int = Query(..., example=245267)
                                ):
    q = crud.mappool.get_mappool(mappool_name)
    if not q:
        return ResCode.raise_error(32301, mappool_name=mappool_name)
    rating = crud.mappool.get_mappool_rating_by_user(q, user_id)
    if not rating:
        return ResCode.raise_error(32303, mappool_name=mappool_name, user_id=user_id)
    crud.mappool.delete_mappool_rating(q, user_id)
    return ResCode.raise_success(41303, mappool_name, user_id)


@router.get('/{mappool_name}/comments',
            summary='获取图池评评论、评论人ID、回复楼层。',
            status_code=status.HTTP_200_OK,
            response_model=List[schemas.mappool.MappoolCommentOut]
            )
async def get_mappool_comments(*,
                               mappool_name: str = Path(..., description='图池名称，只支持全称查询。')
                               ) -> List[dict]:
    q = crud.mappool.get_mappool(mappool_name)
    if not q:
        # return ResCode.raise_error(32301, mappool_name=mappool_name)
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='没有找到对应图池哦！')
    if not q.comments:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='没有查询到相应评价！')
        # return ResCode.raise_error(32303, mappool_name=mappool_name)

    comments = crud.mappool.get_mappool_comments(q)
    return comments


@router.post('/{mappool_name}/comments',
             summary='创建评论。',
             status_code=status.HTTP_201_CREATED)
async def create_mappool_comments(*,
                                  mappool_name: str = Path(..., description='图池名称，只支持全称查询。'),
                                  t: schemas.mappool.MappoolComment
                                  ) -> schemas.RaiseInfo:
    q = crud.mappool.get_mappool(mappool_name)
    if not q:
        return ResCode.raise_error(32301, mappool_name=mappool_name)
    comment = crud.mappool.create_mappool_comment(t)
    crud.mappool.push_comment_to_mappool(q, comment)
    return ResCode.raise_success(11304)


@router.delete('/{mappool_name}/comments',
               summary='删除用户的评论!',
               status_code=status.HTTP_202_ACCEPTED)
async def delete_mappool_rating(*,
                                comment_id: str = Query(..., description='评论的ObjectID，唯一')
                                ):
    comment = MappoolComments.objects(id=comment_id).first()
    if not comment:
        return ResCode.raise_error(32304, comment_id=comment_id)
    crud.mappool.delete_mappool_comment(comment_id)
    return ResCode.raise_success(41304, comment_id)
