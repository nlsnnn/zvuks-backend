from datetime import datetime
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, field_validator

from app.music.schemas import MusicCreate, CoverCreate


class AlbumRead(BaseModel):
    id: int
    name: str
    release_date: str | datetime
    cover_path: str


class AlbumCreate(MusicCreate, CoverCreate):
    songs: list[UploadFile]
    song_names: list[str]
    track_numbers: list[str]
    artist_ids: str

    @field_validator("track_numbers")
    def parse_track_numbers(cls, v):
        return [int(num) for num in v]

    @classmethod
    async def as_form(
        cls,
        name: str = Form(...),
        release_date: str = Form(...),
        cover: UploadFile = File(...),
        songs: list[UploadFile] = File(...),
        song_names: list[str] = Form(...),
        track_numbers: list[str] = Form(...),
        artists_ids: str = Form(...),
    ):
        if not (len(songs) == len(song_names) == len(track_numbers)):
            raise ValueError("Количество файлов, названий и порядков не совпадают")

        return cls(
            name=name,
            release_date=release_date,
            cover=cover,
            songs=songs,
            song_names=song_names,
            track_numbers=track_numbers,
            artists_ids=artists_ids,
        )
