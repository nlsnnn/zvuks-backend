from sqlalchemy import select
from app.dao.base import BaseDAO
from app.music.models import FavoriteAlbum, FavoriteSong
from app.database import async_session_maker


class FavoriteSongDAO(BaseDAO):
    model = FavoriteSong

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(**filter_by)
                .order_by(cls.model.created_at.desc())
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_all_by_song_ids(cls, song_ids: list[int]):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.song_id.in_(song_ids))
            result = await session.execute(query)
            return result.scalars().all()


class FavoriteAlbumDAO(BaseDAO):
    model = FavoriteAlbum

    @classmethod
    async def get_all_by_album_ids(cls, album_ids: list[int]):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.album_id.in_(album_ids))
            result = await session.execute(query)
            return result.scalars().all()
