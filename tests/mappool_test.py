# p = Mappool(mappool_name='Test', host=245276)
# p.save()
#
# m = MappoolDetail(beatmap_id=123456, index=1, selector=245276)
# mod = MappoolMod(HD=[m])
# s = MappoolStage(stage='小组赛', maps=mod, mappool=p)
# s.save()
#
# Mappool.objects(mappool_name='Test').update_one(push__mappools=s)
#
# p = Mappool.objects(mappool_name='Test').first()
#
# for i in p.mappools:
#     i: DynamicDocument
#     print(i.to_json())
