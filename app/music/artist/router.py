from fastapi import APIRouter, HTTPException

from app.users.dependencies import CurrentUserDep
from app.music.artist.service import ArtistService


router = APIRouter(prefix="/artist/me", tags=["Artist"])


@router.get("/songs")
async def get_my_songs(user: CurrentUserDep):
    return await ArtistService.get_my_songs(user)


@router.get("/songs/{song_id}")
async def get_song_info(song_id: int, user: CurrentUserDep):
    try:
        return await ArtistService.get_song_stats(song_id, user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/albums")
async def get_my_albums(user: CurrentUserDep):
    return await ArtistService.get_my_albums(user)


@router.get("/albums/{album_id}")
async def get_album_info(album_id: int, user: CurrentUserDep):
    try:
        return await ArtistService.get_album_stats(album_id, user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
async def dashboard(user: CurrentUserDep):
    pass
