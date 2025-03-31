from app.music.song import SongDAO
from app.music.album import AlbumDAO
from app.music.service import MusicService
from app.music.favorite.dao import FavoriteAlbumDAO, FavoriteSongDAO


class FavoriteService:
    @staticmethod
    async def get_songs(user_id: int):
        favorites = await FavoriteSongDAO.find_all(user_id=user_id)
        favorite_song_ids = [favorite.song_id for favorite in favorites]
        songs = await SongDAO.find_all_by_ids(favorite_song_ids, is_archive=False)
        data = await MusicService.get_songs_dto(songs)
        return data

    @staticmethod
    async def get_albums(user_id: int):
        favorites = await FavoriteAlbumDAO.find_all(user_id=user_id)
        favorite_album_ids = [favorite.album_id for favorite in favorites]
        albums = await AlbumDAO.find_all_by_ids(favorite_album_ids)
        data = MusicService.get_albums_dto(albums)
        return data

    @staticmethod
    async def add_song(song_id: int, user_id: int):
        await FavoriteSongDAO.add(
            song_id=song_id,
            user_id=user_id
        )

    @staticmethod
    async def add_album(album_id: int, user_id: int):
        await FavoriteAlbumDAO.add(
            album_id=album_id,
            user_id=user_id
        )