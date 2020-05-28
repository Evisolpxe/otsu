from typing import List

from app.models.matches import MatchData


class MatchParser:

    def __init__(self, match_data: MatchData.objects):
        self.match_data = match_data.data

    def parse_joined_player(self):
        return [i.get('id') for i in self.match_data.get('users')]

    def parse_result(self):
        return [{'id': i.get('id'),
                 'start_time': i.get('timestamp'),
                 'scoring_type': i.get('game').get('scoring_type'),
                 'mods': i.get('game').get('mods'),
                 'scores': [{'user_id': score.get('user_id'),
                             'accuracy': score.get('accuracy'),
                             'mods': score.get('mods'),
                             'score': score.get('score'),
                             'max_combo': score.get('max_combo'),
                             'slot': score.get('multiplayer')['slot'],
                             'team': score.get('multiplayer')['team'],
                             'passed': score.get('multiplayer')['pass']}
                            for score in i.get('game').get('scores')],
                 'beatmap_id': i.get('game')['beatmap'].get('id', 0)
                 } for i in self.match_data.get('events')
                if i["detail"]["type"] == "other" and len(i['game']['scores']) >= 2
                ]


A = MatchParser(MatchData.objects(match_id=62006639).first())

print(A.parse_result())
