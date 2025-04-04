from fastapi import UploadFile

from app.music.service import MusicService
from app.music.utils import MusicUtils
from app.music.album import AlbumDAO, AlbumCreate, AlbumRead
from app.music.song import SongDAO
from app.users.models import User


class AlbumService:
    @staticmethod
    async def get_album(id: int):
        album = await AlbumDAO.find_one_or_none_by_id(id)
        data = AlbumRead(
            id=album.id,
            name=album.name,
            release_date=album.release_date,
            cover_path=album.cover_path,
        )
        return data
    

    @staticmethod
    async def get_all_albums(archive: bool = False):
        albums = await AlbumDAO.find_all(is_archive=archive)
        data = MusicService.get_albums_dto(albums)
        return data
    

    @staticmethod
    async def get_album_songs(album_id: int):
        songs = await SongDAO.find_all(album_id=album_id)
        data = await MusicService.get_songs_dto(songs)
        return data


    @staticmethod
    async def add_album(album_data: AlbumCreate, user_data: User):
        name = album_data.name
        directory = MusicUtils.get_directory_name('albums', name, user_data)
        cover_path = await MusicService.upload_file(
            album_data.cover, 
            directory,
            ['jpg', 'jpeg', 'png']
        )
        album = await AlbumService.create_album(
            name, 
            cover_path, 
            album_data.release_date, 
            user_data.id
        )

        songs = await AlbumService.save_album_songs(
            album_data.songs, 
            cover_path, 
            album.id, 
            user_data.id, 
            album_data.song_names, 
            album_data.track_numbers,
            directory
        )

        return [album, songs]


    @staticmethod
    async def create_album(name: str, cover_path: str, date: str, user_id: int):
        album = await AlbumDAO.add(
            name=name,
            cover_path=cover_path,
            release_date=date,
            user_id=user_id
        )
        return album
    

    @staticmethod
    async def save_album_songs(
        songs: list[UploadFile], 
        cover_path: str, 
        album_id: int, 
        user_id: int,
        song_names: list[str],
        track_numbers: list[int],
        directory: str
    ):
        songs_added = []
        
        for i, song in enumerate(songs):
            song_path = await MusicService.upload_file(
                song,
                directory,
                ['mp3', 'wav']
            )

            song_orm = await SongDAO.add(
                name=song_names[i],
                track_number=track_numbers[i],
                path=song_path,
                cover_path=cover_path,
                album_id=album_id,
                user_id=user_id
            )

            songs_added.append(song_orm)
        
        data = await MusicService.get_songs_dto(songs_added)
        return data
    

