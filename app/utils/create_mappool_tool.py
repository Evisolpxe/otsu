import json


def parse_mappool(mod_order: list, mod_number: list, beatmap_id: list, selector: int):
    mod_info = zip(mod_order, mod_number)
    r = []
    for mod, num in mod_info:
        for i in range(1, num+1):
            r.append({"beatmap_id": beatmap_id.pop(0),
                      "mod_index": i,
                      "selector": selector,
                      "mods": [mod]})
    return json.dumps(r)
