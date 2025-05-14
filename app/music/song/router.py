from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from app.music.exceptions import SongReadException, SongUpdateException
from app.music.song.service import SongService
from app.users.dependencies import (
    OptionalUserDep,
    CurrentUserDep,
)
from app.music.song import SongCreate, SongUpdate, SongDAO


router = APIRouter(prefix="/song", tags=["Song"])


@router.get("/")
async def get_all_songs(user: OptionalUserDep, archive: Optional[bool] = False):
    data = await SongService.get_songs(archive, user_id=user.id if user else None)
    return {"songs": data}


@router.get("/{song_id}/")
async def get_song(song_id: int, user: OptionalUserDep):
    try:
        return await SongService.get_song(song_id, user_id=user.id if user else None)
    except SongReadException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/")
async def add_song(
    user_data: CurrentUserDep,
    song_data: SongCreate = Depends(SongCreate.as_form),
) -> dict:
    data = await SongService.add_song(song_data, user_data)

    return {
        "id": data.id,
        "name": song_data.name,
        "path": data.path,
        "cover_path": data.cover_path,
    }


@router.patch("/{song_id}/")
async def update_song(song_id: int, data: SongUpdate, user: CurrentUserDep):
    try:
        await SongService.update_song(song_id, data, user)
    except SongUpdateException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"message": "Песня обновлена"}


@router.delete("/{song_id}/")
async def delete_song(song_id: int):
    await SongDAO.delete(id=song_id)
    return {"message": f"Song {song_id} successfull deleted!"}
