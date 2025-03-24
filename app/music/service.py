import uuid
from fastapi import HTTPException, UploadFile

from app.config import get_s3_base_url, get_s3_client
from app.music.dao import AlbumDAO, SongDAO
from app.music.models import Song
from app.music.schemas import SongRead
from app.music.utils import MusicUtils
from app.users.dao import UsersDAO


class MusicService:
    @staticmethod
    async def get_songs(archive: bool = False):
        songs = await SongDAO.find_all(**{
            "is_archive": archive
        })
        
        data = await MusicService.get_songs_dto(songs)
        return data
    
    
    @staticmethod
    async def get_songs_dto(songs: list[Song]):
        user_ids = await MusicService._get_user_ids(songs)

        users = await UsersDAO.find_all_users_by_ids(list(user_ids))
        user_dict = {user.id: user for user in users}

        data = []
        for song in songs:
            author = user_dict.get(song.user_id)
            if not author and song.album_id:
                album = await AlbumDAO.find_one_or_none_by_id(song.album_id)
                author = user_dict.get(album.user_id)
                continue
            
            data.append(SongRead(
                id=song.id,
                name=song.name,
                path=song.path,
                cover_path=song.cover_path,
                release_date=song.release_date,
                is_archive=song.is_archive,
                author=author.username if author else "Unknown"
            ))
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
    async def save_song(song: UploadFile, directory: str) -> dict:
        if not song.filename.endswith('.mp3'):
            raise HTTPException(status_code=400, detail='Формат должен быть MP3')

        file_content = await song.read()
        if not file_content:
            raise HTTPException(status_code=400, detail='Пустой файл')
        
        file_name = f'{uuid.uuid4()}.mp3'
        file_path = f'{directory}/{file_name}'

        s3_client = get_s3_client()

        await s3_client.upload_file(file_content, file_path)
        return file_path
    

    @staticmethod
    async def get_song(path: str):
        s3_client = get_s3_client()
        file = await s3_client.get_file(path)
        return file


    @staticmethod
    async def upload_cover(cover: UploadFile, name: str, directory: str):
        cover_format = MusicUtils.get_file_format(cover)
        cover_content = await cover.read()
        cover_path = f"{directory}/{name}.{cover_format}"

        s3_client = get_s3_client()
        await s3_client.upload_file(cover_content, cover_path)
        return cover_path
    

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
        name: str, 
        directory: str
    ):
        songs_added = []
        
        for song in songs:
            song_path = await MusicService.save_song(song, directory)
            absolute_song_path = get_s3_base_url() + "/" + song_path

            song_orm = await SongDAO.add(
                name=name,
                path=absolute_song_path,
                cover_path=cover_path,
                album_id=album_id,
                user_id=user_id
            )

            songs_added.append(song_orm)
        
        data = await MusicService.get_songs_dto(songs_added)
        return data