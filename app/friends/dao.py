from sqlalchemy import or_, select
from app.dao.base import BaseDAO
from app.friends.models import Friend, FriendStatus
from app.database import async_session_maker


class FriendsDAO(BaseDAO):
    model = Friend

    @classmethod
    async def get_all_friends_id(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(
                or_(
                    cls.model.user_sended_id == user_id,
                    cls.model.user_received_id == user_id
                ),
                cls.model.status == FriendStatus.friends
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