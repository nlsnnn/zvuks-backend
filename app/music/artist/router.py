from fastapi import APIRouter, HTTPException
from loguru import logger

from app.music.artist.exceptions import StatsException
from app.music.artist.schemas import DashboardRead
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
    except StatsException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


@router.get("/albums")
async def get_my_albums(user: CurrentUserDep):
    return await ArtistService.get_my_albums(user)


@router.get("/albums/{album_id}")
async def get_album_info(album_id: int, user: CurrentUserDep):
    try:
        return await ArtistService.get_album_stats(album_id, user)
    except StatsException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


@router.get("/")
async def dashboard(user: CurrentUserDep) -> DashboardRead:
    return await ArtistService.get_dashboard(user)
