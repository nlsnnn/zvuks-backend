from app.dao.base import BaseDAO
from app.music.models import Album, Song


class AlbumDAO(BaseDAO):
    model = Album


class SongDAO(BaseDAO):
    model = Song