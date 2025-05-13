from fastapi import File, Form, UploadFile
from pydantic import BaseModel, field_validator

from app.music.utils import MusicUtils


class MusicCreate(BaseModel):
    name: str = Form(...)
    release_date: str = Form(alias="releaseDate")
    notify_subscribers: bool = Form(default=False)

    @field_validator("release_date")
    def validate_date(cls, v):
        return MusicUtils.validate_release_date(v)


class CoverCreate(BaseModel):
    cover: UploadFile = File(...)
