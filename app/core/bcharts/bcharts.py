import asyncio
from operator import itemgetter
from collections import defaultdict

from typing import List
from app.api.api_v1 import get_all_user_score_aio

# from app.models.users import UserScores

DEFAULT_RANKING_POINT = []


class BCharts:

    def __init__(self,
                 username_list: List[str],
                 beatmap_id_list: List[int],
                 mods: int = 0,
                 ranking_point: list = None):
        self.username_list = username_list
        self.beatmap_id_list = beatmap_id_list
        self.mods = mods
        self.ranking_point = ranking_point if ranking_point else DEFAULT_RANKING_POINT

        self.scores = []
        self.user_points = {}

    async def query_score(self, beatmap_id: int) -> List[dict]:
        return await asyncio.run(get_all_user_score_aio(self.username_list, beatmap_id, self.mods))

    @staticmethod
    def sort_score(scores: List[dict]):
        return sorted(scores, key=itemgetter('score'))

    @staticmethod
    def calc_accuracy(scores: List[dict]):
        return sorted(self.scores, key=itemgetter('score'))

    def add_point(self, sorted_scores: List[dict]):
        for i, v in enumerate(sorted_scores):
            self.user_points[v.get('username')] = self.ranking_point[i]

