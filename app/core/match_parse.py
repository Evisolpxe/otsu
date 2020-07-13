from typing import List
from datetime import datetime

from app.models.mappool import MappoolMap
from app.models.matches import MatchData, Match, EventResult, Score


class MatchParser:

    def __init__(self, match_id: int, match_data: dict):
        self.match_id = match_id
        self.match_data = match_data
        self.result = self.parse_result()
        self.joined_player = self.parse_joined_player()
        self.to_db()

    def parse_joined_player(self):
        return [i.get('id') for i in self.match_data.get('users')]

    def parse_result(self):
        return [{'id': i.get('id'),
                 'start_time': i.get('timestamp'),
                 'scoring_type': i.get('game').get('scoring_type'),
                 'team_type': i.get('game').get('team_type'),
                 'mods': i.get('game').get('mods'),
                 'scores': [{'user_id': score.get('user_id'),
                             'accuracy': score.get('accuracy'),
                             'mods': score.get('mods'),
                             'score': score.get('score'),
                             'max_combo': score.get('max_combo'),
                             'slot': score.get('match', score.get('multiplayer'))['slot'],  # ppysb改了
                             'team': score.get('match', score.get('multiplayer'))['team'],
                             'passed': score.get('match', score.get('multiplayer'))['pass']}
                            for score in i.get('game').get('scores')],
                 'beatmap_id': i.get('game')['beatmap'].get('id', 0)
                 } for i in self.match_data.get('events')
                if i["detail"]["type"] == "other" and len(i.get('game').get('scores', [])) >= 2
                ]

    def to_db(self):
        match = Match(match_id=self.match_id,
                      time=datetime.strptime(self.result[0]['start_time'], '%Y-%m-%dT%H:%M:%S%z'),
                      joined_player=self.joined_player)
        match.save()
        for i in self.result:
            event = EventResult(id=i['id'],
                                mods=i['mods'],
                                scoring_type=i['scoring_type'],
                                team_type=i['team_type'],
                                start_time=datetime.strptime(i['start_time'], '%Y-%m-%dT%H:%M:%S%z'),
                                beatmap_id=i['beatmap_id'],
                                match=match.id)
            red, blue = [], []
            event.save()
            for score in i['scores']:
                if int(score['score']) < 5000:
                    continue
                s = Score(user_id=score['user_id'],
                          accuracy=score['accuracy'],
                          mods=score['mods'],
                          score=score['score'],
                          max_combo=score['max_combo'],
                          slot=score['slot'],
                          team=score['team'],
                          passed=score['passed'],
                          event=event.id)
                s.save()
                self.push_score_to_event(event, s)
                if score['team'] == 'red':
                    red.append(score['score'])
                else:
                    blue.append(score['score'])

            if i['team_type'] == 'team-vs':
                if sum(red) > sum(blue):
                    event.win_team = 'red'
                else:
                    event.win_team = 'blue'
            event.save()
            self.push_event_to_match(match, event)

    @staticmethod
    def push_score_to_event(event: EventResult, score: Score):
        return event.update(push__scores=score)

    @staticmethod
    def push_event_to_match(match: Match, event: EventResult):
        return match.update(push__events=event)
