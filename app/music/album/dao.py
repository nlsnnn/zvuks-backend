from sqlalchemy import select
from app.dao.base import BaseDAO
from app.music.models import Album
from app.database import async_session_maker


class AlbumDAO(BaseDAO):
    model = Album

    @classmethod
    async def search(cls, query: str, limit: int = 10, archive: bool = False):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter(
                    cls.model.name.ilike(f"%{query}%"), cls.model.is_archive == archive
                )  # noqa: E712
                .limit(limit)
            )
            result = await session.execute(query)
            return result.scalars().all()
