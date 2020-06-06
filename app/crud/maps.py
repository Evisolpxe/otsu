from json import loads
from typing import List

from app.api.get import get_map_by_api

from app.models.maps import MapData


def get_beatmap(beatmap_id: int, mod: List[str], refresh: bool = False):
    mod_int = {'NM': 0, 'EZ': 2, 'HR': 16, 'DT': 64, 'HT': 256}
    mod = sum([mod_int[i] for i in mod if i in mod_int.keys()])

    beatmap = MapData.objects(beatmap_id=beatmap_id, mod=mod).first()
    if not beatmap:
        return create_beatmap(beatmap_id, mod)
    if refresh:
        beatmap.delete()
        return create_beatmap(beatmap_id, mod)
    return loads(beatmap.to_json())


def create_beatmap(beatmap_id: int, mod: int = 0):
    try:
        beatmap = MapData(**get_map_by_api(beatmap_id, mods=mod)[0], mod=mod)
        beatmap.save()
        return beatmap
    except KeyError as e:
        print(e)