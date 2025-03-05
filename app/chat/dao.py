from sqlalchemy import select, and_, or_
from app.dao.base import BaseDAO
from app.chat.models import Message
from app.database import async_session_maker


class MessagesDAO(BaseDAO):
    model = Message

    @classmethod
    async def get_messages_between_users(cls, f_user_id: int, s_user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(
                or_(
                    and_(cls.model.sender_id == f_user_id, cls.model.recipient_id == s_user_id),
                    and_(cls.model.sender_id == s_user_id, cls.model.recipient_id == f_user_id)
                )
            ).order_by(cls.model.id)
            result = await session.execute(query)
            return result.scalars().all()