from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, int_pk


class ListenEvent(Base):
    __tablename__ = "listen_events"

    id: Mapped[int_pk]
    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    updated_at: Mapped[None] = None

    __mapper_args__ = {"exclude_properties": ["updated_at"]}
