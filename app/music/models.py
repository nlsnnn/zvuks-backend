from datetime import datetime
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk
from app.users.models import User


class Album(Base):
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(nullable=False)
    cover_path: Mapped[str] = mapped_column(nullable=False)
    release_date: Mapped[datetime]
    is_archive: Mapped[bool] = mapped_column(
        default=False, server_default=text("false")
    )

    user_id: Mapped[User] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))


class Song(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    path: Mapped[str]
    cover_path: Mapped[str]
    release_date: Mapped[datetime] = mapped_column(nullable=True)
    track_number: Mapped[int] = mapped_column(nullable=True)
    is_archive: Mapped[bool] = mapped_column(
        default=False, server_default=text("false")
    )

    user_id: Mapped[User] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    album_id: Mapped[Album] = mapped_column(
        ForeignKey("albums.id", ondelete="CASCADE"), nullable=True
    )

    artists: Mapped[list[User]] = relationship(
        User, secondary="song_artists", back_populates="songs"
    )


class SongArtist(Base):
    __tablename__ = "song_artists"

    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id", ondelete="CASCADE"), primary_key=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)


class FavoriteSong(Base):
    __tablename__ = "favorite_songs"

    user_id: Mapped[User] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    song_id: Mapped[Song] = mapped_column(ForeignKey("songs.id", ondelete="CASCADE"), primary_key=True)

    __mapper_args__ = {
        "exclude_properties": {"updated_at"}
    }


class FavoriteAlbum(Base):
    __tablename__ = "favorite_albums"

    user_id: Mapped[User] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    album_id: Mapped[Album] = mapped_column(ForeignKey("albums.id", ondelete="CASCADE"), primary_key=True)

    __mapper_args__ = {
        "exclude_properties": {"updated_at"}
    }