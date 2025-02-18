from fastapi import APIRouter

from app.music.routers.album import router as album_router
from app.music.routers.song import router as song_router


router = APIRouter(prefix='/music', tags=['Music'])

router.include_router(song_router)
router.include_router(album_router)
