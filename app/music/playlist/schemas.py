from typing import Optional
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field
from app.music.song.schemas import SongRead
from app.users.schemas import SUserRead


class PlaylistCreate(BaseModel):
    name: str
    private: bool
    cover: UploadFile

    @classmethod
    async def as_form(
        cls,
        name: str = Form(...),
        private: bool = Form(...),
        cover: UploadFile = File(...),
    ):
        return cls(
            name=name,
            private=private,
            cover=cover,
        )


class PlaylistUpdate(BaseModel):
    name: Optional[str] = None
    private: Optional[bool] = None
    cover: Optional[UploadFile] = None

    @classmethod
    async def as_form(
        cls,
        name: Optional[str] = Form(default=None),
        private: Optional[bool] = Form(default=None),
        cover: Optional[UploadFile] = File(default=None),
    ):
        return cls(name=name, private=private, cover=cover)


class PlaylistRead(BaseModel):
    name: str
    cover: str
    private: bool
    author: SUserRead
    songs: list[SongRead]


class PlaylistSongAdd(BaseModel):
    playlist_id: int = Field(serialization_alias="playlistId")
    song_id: int = Field(serialization_alias="songId")
