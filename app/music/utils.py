from fastapi import HTTPException, UploadFile
from datetime import datetime
from dateutil import parser


class MusicUtils:
    @staticmethod
    def get_directory_name(type: str, name: str, username: str, id: int | str = None):
        return datetime.now().strftime(f'uploads/{type}/%Y-%m-%d/{username}/{name}')

    def get_song_directory_name(name: str, username: str, id: int | None):
        return MusicUtils.get_directory_name('songs', name, username, id)
    
    def get_album_directory_name(name: str, username: str, id: int | None):
        return MusicUtils.get_directory_name('albums', name, username, id)
    
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
        
