import asyncio
from typing import Optional, List

import aiohttp
import requests

from global_config import OSU_API_TOKEN_V1

BASE_URL = 'https://osu.ppy.sh/api'


def get_match(match_id: int) -> Optional[dict]:
    r = requests.get(f'{BASE_URL}/get_match', params={'k': OSU_API_TOKEN_V1, 'mp': match_id})
    if r.json().get('match'):
        return r.json()


def get_user(user_id: int = None, username: str = None, mode: int = 0) -> Optional[dict]:
    if user_id or username:
        r = requests.get(f'{BASE_URL}/get_user', params={
            'k': OSU_API_TOKEN_V1,
            'u': user_id or username,
            'm': mode
        })
        return r.json()


def get_beatmap():
    pass


def get_user_score(username: str, beatmap_id: int, mods: int = 0):
    r = requests.get(f'{BASE_URL}/get_scores', params={
        'k': OSU_API_TOKEN_V1,
        'b': beatmap_id,
        'u': username,
    })
    return r.json()


async def get_user_score_aio(session: aiohttp.ClientSession, username: str, beatmap_id: int, mods: int = 0):
    async with session.get(f'{BASE_URL}/get_scores', params={
        'k': OSU_API_TOKEN_V1,
        'b': beatmap_id,
        'u': username,
    }) as res:
        data = await res.json()
        return data[0]


async def get_all_user_score_aio(username_list: List[str], beatmap_id: int, mods: int = 0):
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[get_user_score_aio(session, username, beatmap_id, mods)
                                         for username in username_list], return_exceptions=True)
        return results


print(asyncio.run(get_all_user_score_aio(['Explosive', 'rinkon', 'Dsan'], 1849487)))
