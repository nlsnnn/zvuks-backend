from fastapi import File, Form, UploadFile

from app.music.schemas import MusicCreate, CoverCreate


class AlbumCreate(MusicCreate, CoverCreate):
    songs: list[UploadFile]
    song_names: list[str]
    track_numbers: list[str]

    @classmethod
    async def as_form(
        cls,
        name: str = Form(...),
        release_date: str = Form(...),
        cover: UploadFile = File(...),
        songs: list[UploadFile] = File(...),
        song_names: list[str] = Form(...),
        track_numbers: list[int] = Form(...)
    ):
        return cls(
            name=name,
            release_date=release_date,
            cover=cover,
            songs=songs,
            song_names=song_names,
            track_numbers=track_numbers
        )