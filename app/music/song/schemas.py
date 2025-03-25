from datetime import datetime
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field

from app.music.schemas import MusicCreate, CoverCreate


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