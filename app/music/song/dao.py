from app.dao.base import BaseDAO
from app.music.models import Song


class SongDAO(BaseDAO):
    model = Song