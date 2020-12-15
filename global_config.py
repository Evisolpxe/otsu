import os

from dotenv import load_dotenv

load_dotenv()
OSU_API_TOKEN_V1 = os.getenv('OSU_API_TOKEN_V1')
if not OSU_API_TOKEN_V1:
    raise ValueError('Please provide a valid API key.')


# 当前赛季
CURRENT_SEASON = os.getenv('CURRENT_SEASON')
