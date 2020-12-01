from typing import Optional
import requests

from global_config import OSU_API_TOKEN_V1

BASE_URL = 'https://osu.ppy.sh/api/'


def get_match(match_id: int) -> Optional[dict]:
    r = requests.get(f'{BASE_URL}get_match', params={'k': OSU_API_TOKEN_V1, 'mp': match_id})
    if r.json().get('match'):
        return r.json()


def get_user(user_id: int = None, username: str = None, mode: int = 0) -> Optional[dict]:
    if user_id or username:
        r = requests.get(f'{BASE_URL}get_user', params={
            'k': OSU_API_TOKEN_V1,
            'u': user_id or username,
            'm': mode
        })
        return r.json()


def get_beatmap():
    pass

