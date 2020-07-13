import requests

from app.models import users

season = 'Season 0'


def from_old_otsu():
    for i in range(1, 200):
        r = requests.get(f'http://47.101.168.165:5005/api/pages/eloRanking/{i}')
        if not r.json().get('data'):
            break
        for data in r.json().get('data').values():
            print(data)
            users.EloHistory(user_id=data.get('user_id'),
                             elo=data.get('elo'),
                             season=season
                             ).save()


from_old_otsu()
