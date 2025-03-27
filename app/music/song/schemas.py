from datetime import datetime
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field, field_validator

from app.music.schemas import MusicCreate, CoverCreate


class SongUpdate(BaseModel):
    name: str = Field(description="Название песни")
    release_date: datetime = Field(description="Дата релиза песни")


class SongRead(BaseModel):
    id: int
    name: str
    path: str
    cover_path: str
    release_date: str | datetime | None = Field(default=None)
    is_archive: bool
    authors: str


class SongCreate(MusicCreate, CoverCreate):
    song: UploadFile = File(...)
    artist_ids: str = Form(...)

    @field_validator("artist_ids")
    def parse_artist_ids(cls, v):
        return [int(artist_id) for artist_id in v.split(",")]

    @classmethod
    async def as_form(
        cls,
        name: str = Form(...),
        release_date: str = Form(...),
        song: UploadFile = File(...),
        cover: UploadFile = File(...),
        artist_ids: str = Form(...),
    ):
        return cls(
            name=name,
            release_date=release_date,
            song=song,
            cover=cover,
            artist_ids=artist_ids,
        )
