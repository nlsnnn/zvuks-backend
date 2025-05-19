from fastapi import APIRouter

from app.music.favorite.schemas import SFavoriteAlbumRequest, SFavoriteSongRequest
from app.users.dependencies import CurrentUserDep
from app.music.favorite.service import FavoriteService


router = APIRouter(prefix="/favorite", tags=["Favorite"])


@router.get("/song")
async def get_favorite_songs(
    user_data: CurrentUserDep,
):
    songs = await FavoriteService.get_songs(user_data.id)
    return songs


@router.get("/album")
async def get_favorite_albums(
    user_data: CurrentUserDep,
):
    albums = await FavoriteService.get_albums(user_data)
    return albums


@router.post("/song", status_code=201)
async def add_favorite_song(
    data: SFavoriteSongRequest,
    user_data: CurrentUserDep,
):
    await FavoriteService.add_song(data.song_id, user_data.id)


@router.post("/album", status_code=201)
async def add_favorite_album(
    data: SFavoriteAlbumRequest,
    user_data: CurrentUserDep,
):
    await FavoriteService.add_album(data.album_id, user_data.id)


@router.delete("/song", status_code=204)
async def remove_favorite_song(data: SFavoriteSongRequest, user_data: CurrentUserDep):
    await FavoriteService.delete_song(data.song_id, user_data.id)


@router.delete("/album", status_code=204)
async def remove_favorite_album(data: SFavoriteAlbumRequest, user_data: CurrentUserDep):
    await FavoriteService.delete_album(data.album_id, user_data.id)
