from sqlalchemy import and_, or_, select
from app.dao.base import BaseDAO
from app.friends.models import Friend, FriendStatus
from app.database import async_session_maker


class FriendsDAO(BaseDAO):
    model = Friend


    @classmethod
    async def get_friendship(cls, f_user_id: int, s_user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(
                or_(
                    and_(
                        cls.model.user_sended_id==f_user_id,
                        cls.model.user_received_id==s_user_id
                    ),
                    and_(
                        cls.model.user_sended_id==s_user_id,
                        cls.model.user_received_id==f_user_id
                    )
                )
            )
            friendship = await session.execute(query)
            return friendship.scalar()
        
    @staticmethod
    async def get_friendship_status(user_id: int, other_user_id: int):
        friendship = await FriendsDAO.get_friendship(user_id, other_user_id)
        if friendship:
            return friendship.status.value
        
        return "none"


    @classmethod
    async def get_all_friends_id(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(
                or_(
                    cls.model.user_sended_id == user_id,
                    cls.model.user_received_id == user_id
                ),
                cls.model.status == FriendStatus.friends.value
            )
            result = await session.execute(query)
            friendships = result.scalars().all()

            friends = []
            for friendship in friendships:
                if friendship.user_sended_id == user_id:
                    friends.append(friendship.user_received_id)
                else:
                    friends.append(friendship.user_sended_id)

            return friends