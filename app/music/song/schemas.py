from datetime import datetime
from typing import Optional
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field, field_validator

from app.music.schemas import MusicCreate, CoverCreate
from app.users.schemas import SUserRead


class SongUpdate(BaseModel):
    name: Optional[str] = Field(description="Название песни", default=None)
    release_date: datetime = Field(
        description="Дата релиза песни", alias="releaseDate", default=None
    )
    album_id: Optional[int] = Field(alias="albumId", default=None)
    track_number: Optional[int] = Field(alias="trackNumber", default=None)
    is_archive: Optional[int] = Field(alias="archive", default=None)


class SongRead(BaseModel):
    id: int
    name: str = Field(serialization_alias="title")
    path: str
    cover_path: str = Field(serialization_alias="cover")
    release_date: str | datetime | None = Field(
        default=None, serialization_alias="releaseDate"
    )
    is_archive: bool = Field(serialization_alias="archive")
    is_favorite: bool = Field(serialization_alias="favorite")
    artists: list[SUserRead]


class SongCreate(MusicCreate, CoverCreate):
    song: UploadFile = File(...)
    artist_ids: str = Form(alias="artistIds")

    @field_validator("artist_ids")
    def parse_artist_ids(cls, v):
        return [int(artist_id) for artist_id in v.split(",")]

    @classmethod
    async def as_form(
        cls,
        name: str = Form(...),
        release_date: str = Form(alias="releaseDate"),
        notify_subscribers: bool = Form(default=False),
        song: UploadFile = File(...),
        cover: UploadFile = File(...),
        artist_ids: str = Form(alias="artistIds"),
    ):
        return cls(
            name=name,
            release_date=release_date,
            notify_subscribers=notify_subscribers,
            song=song,
            cover=cover,
            artist_ids=artist_ids,
        )
