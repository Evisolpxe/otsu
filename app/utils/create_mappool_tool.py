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
    print(json.dumps(r))


parse_mappool(['NM', 'HD', 'HR', 'DT', 'TB'],
              [7, 5, 5, 5, 1],
              [2182483, 1299913, 1974602, 2321933, 2482069, 2002308, 870323, 1692633, 1863205, 2192488, 1419909,
               2116883, 2452654, 2427894, 614239, 1018938, 1937663, 2025223, 2239032, 2208451, 2048440, 2365667, 2239619
               ],
              245276)
