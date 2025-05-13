from datetime import datetime, timedelta
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from app.dao.base import BaseDAO
from app.music.models import Song
from app.database import async_session_maker
from app.music.recommendations.models import ListenEvent


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

    @classmethod
    async def get_latest(cls, limit: int = 10):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .order_by(cls.model.created_at.desc())
                .limit(limit)
                .options(selectinload(cls.model.artists))
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_to_publish(cls):
        async with async_session_maker() as session:
            now = datetime.now()  # tz =timezone.utc
            query = select(cls.model).filter(
                cls.model.is_archive == True,  # noqa: E712
                cls.model.release_date <= now,
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_listens_count(cls, song_id: int) -> int:
        async with async_session_maker() as session:
            query = select(func.count()).filter(ListenEvent.song_id == song_id)
            result = await session.execute(query)
            return result.scalar() or 0

    @classmethod
    async def get_listens_count_for_songs(cls, song_ids: list[int]) -> int:
        async with async_session_maker() as session:
            query = select(func.count()).filter(ListenEvent.song_id.in_(song_ids))
            result = await session.execute(query)
            return result.scalar() or 0

    @classmethod
    async def get_daily_listens_stats(cls, song_id: int, days: int = 90):
        async with async_session_maker() as session:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            date_trunc = func.date_trunc("day", ListenEvent.created_at).label("date")

            query = (
                select(
                    date_trunc,
                    func.count().label("listens"),
                )
                .filter(
                    ListenEvent.song_id == song_id,
                    ListenEvent.created_at.between(start_date, end_date),
                )
                .group_by(date_trunc)
                .order_by(date_trunc)
            )

            result = await session.execute(query)
            stats = result.all()

            return stats
