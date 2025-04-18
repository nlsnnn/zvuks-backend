from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.dao.base import BaseDAO
from app.music.models import Song
from app.database import async_session_maker


class SongDAO(BaseDAO):
    model = Song

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(**filter_by)
                .options(selectinload(cls.model.artists))
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_all_by_ids(cls, ids: list[int], **filter_by):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .where(cls.model.id.in_(ids))
                .filter_by(**filter_by)
                .options(selectinload(cls.model.artists))
            )
            result = await session.execute(query)
            songs = list(result.scalars().all())
            id_to_song = {song.id: song for song in songs}
            sorted_songs = [id_to_song[id_] for id_ in ids if id_ in id_to_song]
            return sorted_songs
