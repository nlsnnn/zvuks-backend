__all__ = (
    'music_router',
)

from fastapi import APIRouter

from app.music.song.router import router as song_router
from app.music.album.router import router as album_router
from app.music.favorite.router import router as favorite_router


music_router = APIRouter(prefix='/music', tags=['Music'])

music_router.include_router(song_router)
music_router.include_router(album_router)
music_router.include_router(favorite_router)