from datetime import datetime
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field, field_validator

from app.music.utils import MusicUtils


class SongUpdate(BaseModel):
    name: str = Field(description='Название песни')
    release_date: datetime = Field(description='Дата релиза песни')


class SongRead(BaseModel):
    id: int
    name: str
    path: str
    cover_path: str
    release_date: str | datetime | None = Field(default=None)
    is_archive: bool
    author: str


class MusicCreate(BaseModel):
    name: str = Form(...)
    release_date: str = Form(...)

    @field_validator('release_date')
    def validate_date(cls, v):
        return MusicUtils.validate_release_date(v)
    

class CoverCreate(BaseModel):
    cover: UploadFile = File(...)


class SongCreate(MusicCreate, CoverCreate):
    song: UploadFile = File(...)

    @classmethod
    async def as_form(cls, 
        name: str = Form(...),
        release_date: str = Form(...),
        song: UploadFile = File(...),
        cover: UploadFile = File(...)
    ):
        return cls(
            name=name,
            release_date=release_date,
            song=song,
            cover=cover
        )


class AlbumCreate(MusicCreate, CoverCreate):
    songs: list[UploadFile]
    song_names: list[str]

    @classmethod
    async def as_form(
        cls,
        name: str = Form(...),
        release_date: str = Form(...),
        cover: UploadFile = File(...),
        songs: list[UploadFile] = File(...),
        song_names: list[str] = Form(...)
    ):
        return cls(
            name=name,
            release_date=release_date,
            cover=cover,
            songs=songs,
            song_names=song_names
        )