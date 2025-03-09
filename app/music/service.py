import asyncio
from fastapi import UploadFile

from app.config import get_s3_client


class MusicService:
    @staticmethod
    async def save_song(song: UploadFile, cover: UploadFile, song_name: str, username: str) -> dict:
        song_format = song.filename.split('.')[-1]
        cover_format = cover.filename.split('.')[-1]

        song_content = await song.read()
        cover_content = await cover.read()

        s3_client = get_s3_client()
        tasks = [
            s3_client.upload_file(song_content, f"{song_name}.{song_format}"),
            s3_client.upload_file(cover_content, f"{song_name}.{cover_format}")
        ]

        asyncio.gather(
            *tasks
        )

        return {'song_path': 'TEST', 'cover_path': 'TEST'}
