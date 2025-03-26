from fastapi import HTTPException, UploadFile
from datetime import datetime
from dateutil import parser

from app.users.models import User


class MusicUtils:
    @staticmethod
    def get_directory_name(type_: str, name: str, user: User):
        return (
            f"uploads/{type_}/"
            f"{datetime.now().strftime('%Y-%m-%d')}/"
            f"{user.username}_{user.id}/"
            f"{name}"
        )
    
    def get_file_format(file: UploadFile):
        return file.filename.split('.')[-1]

    def validate_release_date(date_str: str) -> datetime:
        try:
            release_date = parser.parse(date_str)
            if release_date.tzinfo:
                raise ValueError("Дата не должна содержать timezone")
            return release_date.replace(tzinfo=None)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Неверный формат даты: {str(e)}")


    def validate_song_format(song: str):
        if song.split('.')[-1] != 'mp3':
            raise HTTPException(
                status_code=400,
                detail='Формат должен быть MP3'
            )
        
