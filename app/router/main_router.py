from fastapi import APIRouter

from .endpoints import matches, users

router = APIRouter()

router.include_router(matches.router, tags=['matches'], prefix='/matches')
router.include_router(users.router, tags=['users'], prefix='/users')
