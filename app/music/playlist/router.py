from typing import Annotated
from fastapi import APIRouter, Depends

from app.music.playlist.schemas import PlaylistCreate, PlaylistSongAdd
from app.users.models import User
from app.users.dependencies import get_current_user, get_current_admin_user
from app.music.playlist.service import PlaylistService


router = APIRouter(prefix="/playlist", tags=["Playlist"])


@router.get("/")
async def get_all_playlists(
    user_data: Annotated[User, Depends(get_current_admin_user)],
):
    return await PlaylistService.get_all_playlists()


@router.get("/{playlist_id}")
async def get_playlist(
    playlist_id: int, user_data: Annotated[User, Depends(get_current_user)]
):
    return await PlaylistService.get_playlist(playlist_id)


@router.post("/")
async def create_playlist(
    data: Annotated[PlaylistCreate, Depends(PlaylistCreate.as_form)],
    user_data: Annotated[User, Depends(get_current_user)],
):
    await PlaylistService.create_playlist(data, user_data)
    return {"message": "Плейлист успешно создан!"}


@router.post("/song")
async def add_playlist_song(
    data: PlaylistSongAdd, user_data: Annotated[User, Depends(get_current_user)]
):
    await PlaylistService.add_playlist_song(data)
    return {"message": "Песня добавлена в плейлист"}
