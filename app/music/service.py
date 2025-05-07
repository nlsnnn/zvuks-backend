from fastapi import UploadFile

from app.music.album.dao import AlbumDAO
from app.music.album.schemas import AlbumRead
from app.music.favorite.dao import FavoriteSongDAO
from app.music.models import Song, Album
from app.music.song import SongRead
from app.services.utils import Utils
from app.users.schemas import SUserRead


class MusicService:
    @staticmethod
    async def get_songs_dto(songs: list[Song], user_id: int | None = None):
        data = []
        favorite_song_ids = []

        if user_id:
            favorites = await FavoriteSongDAO.find_all(user_id=user_id)
            favorite_song_ids = [fav.song_id for fav in favorites]

        for song in songs:
            artists_dto = [
                SUserRead(
                    id=artist.id, username=artist.username, avatar=artist.avatar_path
                )
                for artist in song.artists
            ]

            data.append(
                SongRead(
                    id=song.id,
                    name=song.name,
                    path=song.path,
                    cover_path=song.cover_path,
                    release_date=song.release_date,
                    is_archive=song.is_archive,
                    is_favorite=song.id in favorite_song_ids,
                    artists=artists_dto,
                )
            )
        return data

    @staticmethod
    def get_albums_dto(albums: list[Album]):
        data = [
            AlbumRead(
                id=album.id,
                name=album.name,
                release_date=album.release_date,
                cover_path=album.cover_path,
            )
            for album in albums
        ]
        return data

    @staticmethod
    async def _get_user_ids(songs: list[Song]):
        user_ids = set()
        album_ids = set()

        for song in songs:
            if song.user_id:
                user_ids.add(song.user_id)
            else:
                album_ids.add(song.album_id)

        if album_ids:
            albums = await AlbumDAO.find_all(id=album_ids)
            user_ids.update(album.user_id for album in albums)

        return user_ids

    @staticmethod
    async def upload_file(file: UploadFile, directory: str, allowed_formats: list[str]):
        path = await Utils.upload_file(file, directory, allowed_formats)
        return path
