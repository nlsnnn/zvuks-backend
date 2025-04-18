from datetime import datetime
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field, field_validator

from app.music.schemas import MusicCreate, CoverCreate
from app.users.schemas import SUserRead


class SongUpdate(BaseModel):
    name: str = Field(description="Название песни")
    release_date: datetime = Field(
        description="Дата релиза песни", serialization_alias="releaseDate"
    )


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
        song: UploadFile = File(...),
        cover: UploadFile = File(...),
        artist_ids: str = Form(alias="artistIds"),
    ):
        return cls(
            name=name,
            release_date=release_date,
            song=song,
            cover=cover,
            artist_ids=artist_ids,
        )
