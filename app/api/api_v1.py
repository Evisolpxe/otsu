import asyncio
from typing import Optional, List

import aiohttp
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


async def aio_get_users(user_ids: List[int], mode: int = 0) -> Optional[List[dict]]:
    async def get_users(*args, **kwargs):
        if user_ids:
            user_data = []
            async with aiohttp.ClientSession() as session:
                for user_id in user_ids:
                    async with session.get(
                            f'{BASE_URL}get_user', params={
                                'k': OSU_API_TOKEN_V1,
                                'u': user_id,
                                'm': mode
                            }) as res:
                        user = await res.json()
                        user_data.append(user)
            return user_data

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(get_users([245276, 4504101, 7562902]))
