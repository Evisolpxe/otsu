from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router.main_router import router

app = FastAPI(title='otsu', version='2.01', description='osu!比赛排名系统。')

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
