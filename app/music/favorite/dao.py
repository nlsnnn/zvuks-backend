from app.dao.base import BaseDAO
from app.music.models import FavoriteAlbum, FavoriteSong


class FavoriteSongDAO(BaseDAO):
    model = FavoriteSong


class FavoriteAlbumDAO(BaseDAO):
    model = FavoriteAlbum