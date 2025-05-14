from datetime import datetime, timedelta
from sqlalchemy import select, func, desc
from sqlalchemy.exc import SQLAlchemyError
from app.database import async_session_maker
from app.music.models import FavoriteSong
from app.music.recommendations.models import ListenEvent


class RecommendationsDAO:
    @classmethod
    async def top_by_plays(cls, limit: int = 10) -> list[int]:
        async with async_session_maker() as session:
            # stmt = f"""SELECT le.song_id, count(le.id) as listens from listen_events le group by le.song_id order by listens desc limit {limit}"""
            orm_stmt = (
                select(ListenEvent.song_id, func.count(ListenEvent.id).label("listens"))
                .group_by(ListenEvent.song_id)
                .order_by(desc("listens"))
                .limit(limit)
            )
            result = await session.execute(orm_stmt)

            return result.scalars().all()

    @classmethod
    async def add_listen(cls, song_id: int, user_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = ListenEvent(song_id=song_id, user_id=user_id)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def get_favorites_songs(
        cls, days: int, limit: int = 10, archive: bool = False
    ):
        async with async_session_maker() as session:
            start_date = datetime.now() - timedelta(days=days)
            end_date = datetime.now()

            stmt = (
                select(
                    FavoriteSong.song_id,
                    func.count(FavoriteSong.song_id).label("favorites"),
                )
                .group_by(FavoriteSong.song_id)
                .filter(FavoriteSong.created_at.between(start_date, end_date))
                .order_by(desc("favorites"))
                .limit(limit)
            )
            result = await session.execute(stmt)
            return result.scalars().all()
