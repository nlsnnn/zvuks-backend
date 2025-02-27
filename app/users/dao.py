from sqlalchemy import select
from app.dao.base import BaseDAO
from app.users.models import User
from app.database import async_session_maker


class UsersDAO(BaseDAO):
    model = User


    @classmethod
    async def find_all_users_by_ids(cls, ids: list[int]):
        async with async_session_maker() as session:
            query = select(cls.model).where(
                cls.model.id.in_(ids)
            )
            result = await session.execute(query)
            users = result.scalars().all()
            return users
        
    @classmethod
    async def search_users(cls, query: str):
        async with async_session_maker() as session:
            search_query = f"%{query}%"
            stmt = select(cls.model).where(
                cls.model.username.ilike(search_query)
            )
            result = await session.execute(stmt)
            return result.scalars().all()