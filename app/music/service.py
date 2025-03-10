import asyncio
from datetime import datetime
from mutagen.mp3 import MP3
from fastapi import UploadFile

from app.config import get_s3_client


class MusicService:
    @staticmethod
    async def save_song(song: UploadFile, cover: UploadFile, song_name: str, username: str) -> dict:
        directory = datetime.now().strftime(f'uploads/songs/%Y-%m-%d/{username}')
        
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
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(f'https://storage.yandexcloud.net/zvuks-backet/{path}') as resp:
        #         # print(resp.status)
        #         print(f'{resp=}')
        #         print(await resp.text())
        #         return resp.content

        s3_client = get_s3_client()
        file = await s3_client.get_file(path)
        print(f'{file=}')
        print(f'{type(file)=}')
        return file
    

    @staticmethod
    def get_audio_duration(file) -> float:
        audio = MP3(file)
        return audio.info.length