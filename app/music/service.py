import asyncio
from datetime import datetime
from fastapi import UploadFile

from app.config import get_s3_client
from app.music.dao import AlbumDAO, SongDAO
from app.music.models import Song
from app.music.schemas import SongRead
from app.music.utils import get_file_format
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
    async def get_songs_dto(songs: Song):
        author_ids = [song.user_id for song in songs]
        authors = list(await UsersDAO.find_all_users_by_ids(author_ids))
        data = []

        for i in range(len(songs)):
            song = songs[i]
            author = authors[i]
            print(f'{i=}')
            print(f'{song=}')
            print(f'{author=}\n')

            if song.user_id == author.id: # TODO переделать алгоритм 
                authors.insert(i, author)
            
            data.append(
                SongRead(
                    id=song.id,
                    name=song.name,
                    path=song.path,
                    cover_path=song.cover_path,
                    release_date=song.release_date,
                    is_archive=song.is_archive,
                    author=author.username
                )
            )

        return data


    @staticmethod
    async def save_song(song: UploadFile, song_name: str, directory: str) -> dict:
        song_format = song.filename.split('.')[-1]
        song_content = await song.read()
        song_path = f"{directory}/{song_name}.{song_format}"

        s3_client = get_s3_client()

        await s3_client.upload_file(song_content, song_path)

        return song_path
    

    @staticmethod
    async def get_song(path: str):
        s3_client = get_s3_client()
        file = await s3_client.get_file(path)
        return file


    @staticmethod
    async def upload_cover(cover: UploadFile, name: str, directory: str):
        cover_format = get_file_format(cover)
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
        name: str, 
        directory: str
    ):
        songs_added = []
        
        for song in songs:
            song_path = await MusicService.save_song(song, name, directory)

            song_orm = await SongDAO.add(
                name=name,
                path=song_path,
                cover_path=cover_path,
                album_id=album_id
            )

            songs_added.append(song_orm)
        
        data = await MusicService.get_songs_dto(songs_added)
        return data