from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, int_pk


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int_pk]
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id")) #, ondelete='CASCADE'))
    recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)