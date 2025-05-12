from app.music.album.schemas import AlbumRead
from app.music.song.schemas import SongRead


class SongStatsRead(SongRead):
    favorites: int
    listens: int


class AlbumStatsRead(AlbumRead):
    favorites: int
    listens: int
