from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from app.dao.base import BaseDAO
from app.music.models import Playlist, PlaylistSong, Song
from app.database import async_session_maker


class PlaylistDAO(BaseDAO):
    model = Playlist

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(**filter_by)
                .options(
                    joinedload(cls.model.user),
                    selectinload(cls.model.songs).options(selectinload(Song.artists)),
                )
            )
            result = await session.execute(query)
            return result.unique().scalars().all()


class PlaylistSongDAO(BaseDAO):
    model = PlaylistSong
