from typing import Optional
import requests

from global_config import OSU_V1_API_TOKEN

BASE_URL = 'https://osu.ppy.sh/api/'


def get_match(match_id: int) -> Optional[dict]:
    r = requests.get(f'{BASE_URL}get_match', params={'k': OSU_V1_API_TOKEN, 'mp': match_id})
    if r.json().get('match'):
        return r.json()


