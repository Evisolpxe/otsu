import requests
from requests.exceptions import ConnectTimeout

BASE_URL = 'https://osu.ppy.sh/api'
TOKEN = '9aa58c3820b6a95beb5b4430df5f88f5812cdaf1'


def get_match_by_history(match_id: int) -> dict:
    # mplink页面的源api，过长的比赛返回数据会不完整，需要多次请求拼接数据。
    # 更改limit值似乎无用。
    url = f"https://osu.ppy.sh/community/matches/{match_id}/history?limit=100"
    retry = 0
    # ppy服务器会莫名的崩掉...
    while retry < 3:
        try:
            r = requests.get(url, timeout=5)
        except ConnectTimeout as err:
            retry += 1
            print(f'Connect failed, try again. Times: {retry}')
        else:
            data = r.json()
            print(f'获取{match_id}成功。')
            break
    # 检测返回的数据是否完整，不完整就再请求一次。
    while data['events'][0]['detail']['type'] != 'match-created':
        print('数据不完整，再次请求补全。')
        r2 = requests.get(
            f"https://osu.ppy.sh/community/matches/{match_id}/history?before={data['events'][0]['id']}")
        before_data = r2.json()
        before_data['events'].extend(data['events'])
        before_data['users'].extend(data['users'])
        data = before_data
    return data


def get_map_by_api(map_id: int, mods: int = 0) -> dict:
    retry = 0
    while retry < 5:
        try:
            r = requests.get(f"{BASE_URL}/get_beatmaps?k={TOKEN}&b={map_id}&mods={mods}")
            print(f"{BASE_URL}/get_beatmaps?k={TOKEN}&b={map_id}&mods={mods}")
            print(r.json())
        except ConnectTimeout as err:
            retry += 1
            print(f'Connect failed, try again. Times: {retry}')
        else:
            break
    if not r.json():
        return
    return r.json()


def get_user_by_api(user_id: int) -> dict:
    r = requests.post(f"{BASE_URL}/get_user",
                      {'k': TOKEN, 'u': user_id})
    return r.json()
    # while retry < 5:
    #     try:
    #         r = requests.post(f"{BASE_URL}/get_user",
    #                           {'k': TOKEN, 'u': user_id})
    #     except ConnectTimeout as err:
    #         retry += 1
    #         print(f'Connect failed, try again. Times: {retry}')
    #     else:
    #         break
    #     # 忘记当时为啥这么写了。
    # if not r.json():
    #     return

