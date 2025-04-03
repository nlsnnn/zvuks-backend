from pydantic import BaseModel


class SFavoriteSongRequest(BaseModel):
    song_id: int


class SFavoriteAlbumRequest(BaseModel):
    album_id: int