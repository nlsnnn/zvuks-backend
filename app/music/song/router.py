from typing import Optional
from fastapi import APIRouter, Depends, HTTPException

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
async def get_song(song_id: int):
    song = await SongDAO.find_one_or_none_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    return {"song_path": song.path, "cover_path": song.cover_path}


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


@router.put("/{song_id}/")
async def update_song(song_id: int, data: SongUpdate):
    song = await SongDAO.find_one_or_none_by_id(song_id)
    return {"ok": "ok"}


@router.delete("/{song_id}/")
async def delete_song(song_id: int):
    await SongDAO.delete(id=song_id)
    return {"message": f"Song {song_id} successfull deleted!"}
