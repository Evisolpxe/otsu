import requests
from requests.exceptions import ConnectTimeout


def get_match_by_history(match_id: int) -> dict:
    # mplink页面的源api，过长的比赛返回数据会不完整，需要多次请求拼接数据。
    # 更改limit值似乎无用。
    url = f"https://osu.ppy.sh/community/matches/{match_id}/history?limit=100"
    retry = 0

    # ppy服务器会莫名的崩掉...
    while retry < 3:
        try:
            print('try')
            r = requests.get(url, timeout=5)
        except ConnectTimeout as err:
            print(f'Connect failed, try again. Times: {retry}')
        else:
            break
    data = r.json()
    # 检测返回的数据是否完整，不完整就再请求一次。
    while data['events'][0]['detail']['type'] != 'match-created':
        print('Incomplete data, request again.')
        r2 = requests.get(
            f"https://osu.ppy.sh/community/matches/{match_id}/history?before={data['events'][0]['id']}")
        before_data = r2.json()
        before_data['events'].extend(data['events'])
        before_data['users'].extend(data['users'])
        data = before_data
    return data