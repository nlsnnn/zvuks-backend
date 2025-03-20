import asyncio
from datetime import datetime
from fastapi import UploadFile

from app.config import get_s3_client
from app.music.dao import SongDAO
from app.music.schemas import SongRead
from app.users.dao import UsersDAO


class MusicService:
    @staticmethod
    async def get_songs(archive: bool = False):
        songs = await SongDAO.find_all(**{
            "is_archive": archive
        })

        author_ids = [song.user_id for song in songs]
        authors = list(await UsersDAO.find_all_users_by_ids(author_ids))
        data = []

        for i in range(len(songs)):
            song = songs[i]
            author = authors[i]

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
    async def save_song(song: UploadFile, cover: UploadFile, song_name: str, username: str) -> dict:
        directory = datetime.now().strftime(f'uploads/songs/%Y-%m-%d/{username}/{song_name}')

        song_format = song.filename.split('.')[-1]
        cover_format = cover.filename.split('.')[-1]

        song_content = await song.read()
        cover_content = await cover.read()

        song_path = f"{directory}/{song_name}.{song_format}"
        cover_path = f"{directory}/{song_name}.{cover_format}"

        s3_client = get_s3_client()

        asyncio.gather(
            s3_client.upload_file(song_content, song_path),
            s3_client.upload_file(cover_content, cover_path)
        )

        return {'song_path': song_path, 'cover_path': cover_path}

    @staticmethod
    async def get_song(path: str):
        s3_client = get_s3_client()
        file = await s3_client.get_file(path)
        return file
