import json
from datetime import datetime
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field

from app.music.schemas import MusicCreate, CoverCreate
from app.users.schemas import SUserRead


class AlbumRead(BaseModel):
    id: int
    name: str = Field(serialization_alias="title")
    release_date: str | datetime = Field(serialization_alias="releaseDate")
    cover_path: str = Field(serialization_alias="cover")
    artist: SUserRead


class AlbumCreate(MusicCreate, CoverCreate): # TODO: refactor
    songs: list[UploadFile]
    song_names: list[str]
    track_numbers: list[int]
    song_artists_ids: list[list[int]]

    @classmethod
    async def as_form(
        cls,
        name: str = Form(alias="title"),
        release_date: str = Form(alias="releaseDate"),
        cover: UploadFile = File(...),
        songs: list[UploadFile] = File(...),
        song_names: list[str] = Form(alias="songNames"),
        track_numbers: list[int] = Form(
            alias="trackNumbers", description="Порядковый номер трека в альбоме"
        ),
        song_artists_ids: str = Form(
            alias="songArtistsIds", description="Артисты на треке"
        ),
    ):
        try:
            parsed_song_artists_ids = json.loads(song_artists_ids)
            if not isinstance(parsed_song_artists_ids, list):
                raise ValueError("songArtistsIds должен быть списком")
        except json.JSONDecodeError:
            raise ValueError("Неверный формат JSON для songArtistsIds")

        if not (
            len(songs)
            == len(song_names)
            == len(track_numbers)
            == len(parsed_song_artists_ids)
        ):
            raise ValueError(
                "Количество файлов, названий, порядков и артистов не совпадают"
            )

        return cls(
            name=name,
            release_date=release_date,
            cover=cover,
            songs=songs,
            song_names=song_names,
            track_numbers=track_numbers,
            song_artists_ids=parsed_song_artists_ids,
        )
