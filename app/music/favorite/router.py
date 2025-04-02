from typing import Annotated
from fastapi import APIRouter, Depends

from app.music.favorite.schemas import SFavoriteRequest
from app.users.dependencies import TokenDepends
from app.users.models import User
from app.music.favorite.service import FavoriteService


router = APIRouter(prefix="/favorite", tags=["Favorite"])

token_depends = TokenDepends()


@router.get("/song")
async def get_favorite_songs(
    user_data: Annotated[User, Depends(token_depends.get_current_user)],
):
    songs = await FavoriteService.get_songs(user_data.id)
    return songs


@router.get("/album")
async def get_favorite_albums(
    user_data: Annotated[User, Depends(token_depends.get_current_user)],
):
    albums = await FavoriteService.get_albums(user_data.id)
    return albums


@router.post("/song", status_code=201)
async def add_favorite_song(
    data: SFavoriteRequest,
    user_data: Annotated[User, Depends(token_depends.get_current_user)],
):
    await FavoriteService.add_song(data.song_id, user_data.id)


@router.post("/album", status_code=201)
async def add_favorite_album(
    data: SFavoriteRequest,
    user_data: Annotated[User, Depends(token_depends.get_current_user)],
):
    await FavoriteService.add_album(data.album_id, user_data.id)


@router.delete("/song", status_code=204)
async def remove_favorite_song(
    data: SFavoriteRequest,
    user_data: Annotated[User, Depends(token_depends.get_current_user)]
):
    await FavoriteService.delete_song(data.song_id, user_data.id)


@router.delete("/album", status_code=204)
async def remove_favorite_album(
    data: SFavoriteRequest,
    user_data: Annotated[User, Depends(token_depends.get_current_user)]
):
    await FavoriteService.delete_album(data.album_id, user_data.id)
