from fastapi import FastAPI, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from app import router

app = FastAPI(title='Otsu-api', version='0.2.0',description='我还要更多的elo...',)

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

app.include_router(router.matches.router, tags=['Matches'], prefix='/matches')
app.include_router(router.tourney.router, tags=['Tourney'], prefix='/tourney')
app.include_router(router.mappool.router, tags=['Mappool'], prefix='/mappool')
