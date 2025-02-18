from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, int_pk
from enum import Enum as PyEnum


class FriendStatus(PyEnum):
    pending = 'pending'
    friends = 'friends'
    deleted = 'deleted'


class Friend(Base):
    id: Mapped[int_pk]
    status: Mapped[FriendStatus] = mapped_column(
        Enum(FriendStatus),
        default=FriendStatus.pending.value,
        server_default=FriendStatus.pending.value
    )
    user_sended_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    user_received_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )