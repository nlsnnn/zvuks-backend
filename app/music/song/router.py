from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request

from app.music.song.service import SongService
from app.users.dependencies import get_current_user
from app.music.song import SongCreate, SongUpdate, SongDAO
from app.users.models import User


router = APIRouter(prefix="/song", tags=["Song"])


@router.get("/")
async def get_all_songs(request: Request, archive: Optional[bool] = False):
    data = await SongService.get_songs(request, archive)
    return {"songs": data}


@router.get("/{song_id}/")
async def get_song(song_id: int):
    song = await SongDAO.find_one_or_none_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    return {"song_path": song.path, "cover_path": song.cover_path}


@router.post("/")
async def add_song(
    song_data: SongCreate = Depends(SongCreate.as_form),
    user_data: User = Depends(get_current_user),
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
