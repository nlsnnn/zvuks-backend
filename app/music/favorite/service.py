from app.exceptions import AlreadyExistsException
from app.music.album.schemas import AlbumRead
from app.music.song import SongDAO
from app.music.album import AlbumDAO
from app.music.service import MusicService
from app.music.favorite.dao import FavoriteAlbumDAO, FavoriteSongDAO
from app.users.models import User
from app.users.schemas import SUserRead


class FavoriteService:
    @staticmethod
    async def get_songs(user_id: int):
        favorites = await FavoriteSongDAO.find_all(user_id=user_id)
        favorite_song_ids = [favorite.song_id for favorite in favorites]
        songs = await SongDAO.find_all_by_ids(favorite_song_ids, is_archive=False)
        data = await MusicService.get_songs_dto(songs, user_id)
        return data

    @staticmethod
    async def get_albums(user: User):
        favorites = await FavoriteAlbumDAO.find_all(user_id=user.id)
        favorite_album_ids = [favorite.album_id for favorite in favorites]
        albums = await AlbumDAO.find_all_by_ids(favorite_album_ids)
        data = [
            AlbumRead(
                id=album.id,
                name=album.name,
                release_date=album.release_date,
                cover_path=album.cover_path,
                favorite=True,
                artist=SUserRead(
                    id=user.id, username=user.username, avatar=user.avatar_path
                ),
            )
            for album in albums
        ]

        return data

    @staticmethod
    async def add_song(song_id: int, user_id: int):
        song = await FavoriteSongDAO.find_one_or_none(
            song_id=song_id,
            user_id=user_id,
        )
        if song:
            raise AlreadyExistsException

        await FavoriteSongDAO.add(song_id=song_id, user_id=user_id)

    @staticmethod
    async def add_album(album_id: int, user_id: int):
        album = await FavoriteAlbumDAO.find_one_or_none(
            album_id=album_id, user_id=user_id
        )
        if album:
            raise AlreadyExistsException

        await FavoriteAlbumDAO.add(album_id=album_id, user_id=user_id)

    @staticmethod
    async def delete_song(song_id: int, user_id: int):
        await FavoriteSongDAO.delete(
            song_id=song_id,
            user_id=user_id,
        )

    @staticmethod
    async def delete_album(album_id: int, user_id: int):
        await FavoriteAlbumDAO.delete(
            album_id=album_id,
            user_id=user_id,
        )
