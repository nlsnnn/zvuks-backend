from app.dao.base import BaseDAO
from app.music.models import Album


class AlbumDAO(BaseDAO):
    model = Album