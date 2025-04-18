from sqlalchemy import select
from app.dao.base import BaseDAO
from app.music.models import FavoriteAlbum, FavoriteSong
from app.database import async_session_maker


class FavoriteSongDAO(BaseDAO):
    model = FavoriteSong

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by).order_by(cls.model.created_at.desc())
            result = await session.execute(query)
            return result.scalars().all()


class FavoriteAlbumDAO(BaseDAO):
    model = FavoriteAlbum