from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router.main_router import router
from global_config import CURRENT_SEASON

app = FastAPI(title='otsu', version='0.21', description=f'osu!比赛排名系统，当前赛季 {CURRENT_SEASON}。')

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
