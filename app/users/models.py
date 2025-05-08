from sqlalchemy import text
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
    playlists: Mapped[list["Playlist"]] = relationship(
        back_populates="user"
    )
    albums: Mapped[list["Album"]] = relationship(
        back_populates="user"
    )
    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
