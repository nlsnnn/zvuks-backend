from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel, Field, field_validator

from app.music.utils import MusicUtils


# class SongAdd(BaseModel):
#     name: str = Form(description='Название песни')
#     release_date: datetime = Form(description='Дата релиза песни')
#     song: UploadFile = File(description="Файл песни")


class AlbumAdd(BaseModel):
    name: str = Field(description='Название песни')
    release_date: datetime = Field(description='Дата релиза песни')


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


class AlbumCreate(BaseModel):
    name: str
    release_date: str
    cover: UploadFile
    songs: list[UploadFile]
    song_names: list[str]
    
    @field_validator('release_date')
    def validate_date(cls, v):
        return MusicUtils.validate_release_date(v)