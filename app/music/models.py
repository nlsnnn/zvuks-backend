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

    user: Mapped[User] = relationship(back_populates="albums", lazy="joined")


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
        User, secondary="song_artists", back_populates="songs", lazy="selectin"
    )
    playlists: Mapped[list["Playlist"]] = relationship(
        secondary="playlist_songs", back_populates="songs"
    )
    user: Mapped[User] = relationship(back_populates="user_songs", lazy="selectin")


class SongArtist(Base):
    __tablename__ = "song_artists"

    song_id: Mapped[int] = mapped_column(
        ForeignKey("songs.id", ondelete="CASCADE"), primary_key=True
    )
    artist_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )


class FavoriteSong(Base):
    __tablename__ = "favorite_songs"

    user_id: Mapped[User] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    song_id: Mapped[Song] = mapped_column(
        ForeignKey("songs.id", ondelete="CASCADE"), primary_key=True
    )

    __mapper_args__ = {"exclude_properties": {"updated_at"}}

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(user_id={self.user_id}, song_id={self.song_id})"
        )


class FavoriteAlbum(Base):
    __tablename__ = "favorite_albums"

    user_id: Mapped[User] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    album_id: Mapped[Album] = mapped_column(
        ForeignKey("albums.id", ondelete="CASCADE"), primary_key=True
    )

    __mapper_args__ = {"exclude_properties": {"updated_at"}}

    def __repr__(self):
        return f"{self.__class__.__name__}(user_id={self.user_id}, album_id={self.album_id})"


class Playlist(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    cover_path: Mapped[str]
    private: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped[User] = relationship(back_populates="playlists", lazy="joined")
    songs: Mapped[list[Song]] = relationship(
        secondary="playlist_songs", back_populates="playlists", lazy="selectin"
    )


class PlaylistSong(Base):
    __tablename__ = "playlist_songs"

    song_id: Mapped[int] = mapped_column(
        ForeignKey("songs.id", ondelete="CASCADE"), primary_key=True
    )
    playlist_id: Mapped[int] = mapped_column(
        ForeignKey("playlists.id", ondelete="CASCADE"), primary_key=True
    )
    created_at: Mapped[None] = None
    updated_at: Mapped[None] = None

    __mapper_args__ = {"exclude_properties": ["created_at", "updated_at"]}
