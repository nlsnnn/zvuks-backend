from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk


class User(Base):
    id: Mapped[int_pk]
    username: Mapped[str_uniq]
    email: Mapped[str_uniq]
    password: Mapped[str]
    bio: Mapped[str] = mapped_column(nullable=True)
    avatar_path: Mapped[str] = mapped_column(nullable=True)

    is_user: Mapped[bool] = mapped_column(
        default=True, server_default=text("true"), nullable=False
    )
    is_admin: Mapped[bool] = mapped_column(
        default=False, server_default=text("false"), nullable=False
    )

    songs: Mapped[list["Song"]] = relationship(
        "Song", secondary="song_artists", back_populates="artists"
    )
    playlists: Mapped[list["Playlist"]] = relationship(back_populates="user")
    albums: Mapped[list["Album"]] = relationship(back_populates="user")
    subscribers: Mapped[list["ArtistSubscriber"]] = relationship(
        "ArtistSubscriber",
        foreign_keys="[ArtistSubscriber.artist_id]",
        back_populates="artist",
    )
    subscriptions: Mapped[list["ArtistSubscriber"]] = relationship(
        "ArtistSubscriber",
        foreign_keys="[ArtistSubscriber.subscriber_id]",
        back_populates="subscriber",
    )
    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class ArtistSubscriber(Base):
    __tablename__ = "artist_subscribers"

    subscriber_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    artist_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    subscriber: Mapped[User] = relationship(
        "User", foreign_keys=[subscriber_id], back_populates="subscriptions"
    )
    artist: Mapped[User] = relationship(
        "User", foreign_keys=[artist_id], back_populates="subscribers"
    )
