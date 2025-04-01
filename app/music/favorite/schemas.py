from pydantic import BaseModel, Field


class SFavoriteRequest(BaseModel):
    song_id: int | None = Field(default=None)
    album_id: int | None = Field(default=None)