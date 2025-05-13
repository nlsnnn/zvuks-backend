from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.dao.base import BaseDAO
from app.friends.dao import FriendsDAO
from app.users.models import User, ArtistSubscriber
from app.database import async_session_maker


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(id=data_id)
                .options(
                    selectinload(cls.model.subscribers),
                    selectinload(cls.model.subscriptions),
                )
            )
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            return user

    @classmethod
    async def search_users(cls, query: str):
        async with async_session_maker() as session:
            search_query = f"%{query}%"
            stmt = select(cls.model).where(cls.model.username.ilike(search_query))
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def search_users_with_status(cls, query: str, current_user_id: int):
        users = await cls.search_users(query)
        users_with_status = []
        for user in users:
            status = await FriendsDAO.get_friendship_status(current_user_id, user.id)
            users_with_status.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "avatar": user.avatar_path,
                    "status": status,
                }
            )

        return users_with_status


class ArtistSubscriberDAO(BaseDAO):
    model = ArtistSubscriber
