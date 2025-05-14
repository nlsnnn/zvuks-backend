from pydantic import BaseModel, Field
from app.music.album.schemas import AlbumRead
from app.music.song.schemas import SongRead


class DailyStat(BaseModel):
    date: str
    listens: int


class SongStatsRead(SongRead):
    favorites: int
    listens: int
    daily_stats: list[DailyStat] = Field(serialization_alias="dailyStats")


class AlbumStatsRead(AlbumRead):
    favorites: int
    listens: int
    daily_stats: list[DailyStat] = Field(serialization_alias="dailyStats")


class DashboardRead(BaseModel):
    listens: int
    subscribers: int
    songs: int
    albums: int
    favorite_songs: int = Field(serialization_alias="favoriteSongs")
    favorite_albums: int = Field(serialization_alias="favoriteAlbums")
