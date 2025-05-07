from typing import Annotated
from fastapi import APIRouter, Depends

from app.music.playlist.schemas import PlaylistCreate, PlaylistSongAdd, PlaylistUpdate
from app.music.playlist.service import PlaylistService
from app.users.dependencies import CurrentUserDep


router = APIRouter(prefix="/playlist", tags=["Playlist"])


@router.get("/")
async def get_all_playlists(user_data: CurrentUserDep):
    return await PlaylistService.get_all_playlists()


@router.get("/{playlist_id}")
async def get_playlist(playlist_id: int, user_data: CurrentUserDep):
    return await PlaylistService.get_playlist(playlist_id)


@router.get("/user/{user_id}")
async def get_user_playlists(user_id: int, user_data: CurrentUserDep):
    return await PlaylistService.get_user_playlists(user_id, user_data)


@router.post("/")
async def create_playlist(
    data: Annotated[PlaylistCreate, Depends(PlaylistCreate.as_form)],
    user_data: CurrentUserDep,
):
    await PlaylistService.create_playlist(data, user_data)
    return {"message": "Плейлист успешно создан"}


@router.patch("/{playlist_id}")
async def update_playlist(
    playlist_id: int,
    data: Annotated[PlaylistUpdate, Depends(PlaylistUpdate.as_form)],
    user_data: CurrentUserDep,
):
    await PlaylistService.update_playlist(playlist_id, data, user_data)
    return {"message": "Плейлист обновлен"}


@router.delete("/{playlist_id}")
async def delete_playlist(playlist_id: int, user_data: CurrentUserDep):
    await PlaylistService.delete_playlist(playlist_id, user_data)
    return {"message": "Плейлист удален"}


@router.post("/song")
async def add_playlist_song(data: PlaylistSongAdd, user_data: CurrentUserDep):
    await PlaylistService.add_playlist_song(data)
    return {"message": "Песня добавлена в плейлист"}


@router.delete("/song/")
async def delete_playlist_song(data: PlaylistSongAdd, user_data: CurrentUserDep):
    await PlaylistService.delete_playlist_song(data, user_data)
    return {"message": "Песня удалена из плейлиста"}
