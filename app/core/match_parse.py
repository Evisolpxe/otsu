from typing import List

from app import models


class MatchParser:

    def __init__(self, match_data: models.MatchData.objects):
        self.match_data = match_data.data

    def parse_user(self):
        print(self.match_data.get('users'))


A = MatchParser(models.MatchData.objects(match_id=61570715).first())

A.parse_user()
