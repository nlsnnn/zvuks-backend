from typing import Annotated
from fastapi import APIRouter, Depends

from app.music.playlist.schemas import PlaylistCreate, PlaylistSongAdd, PlaylistUpdate
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


@router.get("/user/{user_id}")
async def get_user_playlists(
    user_id: int, user_data: Annotated[User, Depends(get_current_user)]
):
    return await PlaylistService.get_user_playlists(user_id, user_data)


@router.post("/")
async def create_playlist(
    data: Annotated[PlaylistCreate, Depends(PlaylistCreate.as_form)],
    user_data: Annotated[User, Depends(get_current_user)],
):
    await PlaylistService.create_playlist(data, user_data)
    return {"message": "Плейлист успешно создан"}


@router.patch("/{playlist_id}")
async def update_playlist(
    playlist_id: int,
    data: Annotated[PlaylistUpdate, Depends(PlaylistUpdate.as_form)],
    user_data: Annotated[User, Depends(get_current_user)],
):
    await PlaylistService.update_playlist(playlist_id, data, user_data)
    return {"message": "Плейлист обновлен"}


@router.delete("/{playlist_id}")
async def delete_playlist(
    playlist_id: int, user_data: Annotated[User, Depends(get_current_user)]
):
    await PlaylistService.delete_playlist(playlist_id, user_data)
    return {"message": "Плейлист удален"}


@router.post("/song")
async def add_playlist_song(
    data: PlaylistSongAdd, user_data: Annotated[User, Depends(get_current_user)]
):
    await PlaylistService.add_playlist_song(data)
    return {"message": "Песня добавлена в плейлист"}


@router.delete("/song/{song_id}")
async def delete_playlist_song(
    data: PlaylistSongAdd, user_data: Annotated[User, Depends(get_current_user)]
):
    await PlaylistService.delete_playlist_song(data, user_data)
    return {"message": "Песня удалена из плейлиста"}
