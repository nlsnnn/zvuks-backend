import aiofiles
import aiofiles.os
from datetime import datetime

from fastapi import HTTPException, UploadFile


async def create_song_directory(song_name: str, username: str):
    path = datetime.now().strftime(f'uploads/songs/%Y-%m-%d/{username}_{song_name}')
    await aiofiles.os.makedirs(path, exist_ok=True)
    return path


async def create_album_directory(album_name: str, username: str):
    path = datetime.now().strftime(f'uploads/albums/%Y-%m-%d/{username}_{album_name}')
    await aiofiles.os.makedirs(path, exist_ok=True)
    return path


async def save_cover(cover: UploadFile, path: str, name: str):
    cover_format = cover.filename.split('.')[-1]
    print(f'{cover_format=}')
    cover_path = f'{path}/{name}.{cover_format}'
    print(f'{cover_path=}')

    async with aiofiles.open(cover_path, 'wb+') as cover_object:
        await cover_object.write(await cover.read())

    return cover_path


async def save_song(song: UploadFile, cover: UploadFile, song_name: str, username: str) -> dict:
    validate_song_format(song.filename)

    directory = await create_song_directory(song_name, username)

    song_path = f'{directory}/{song_name}.mp3'
    cover_path = await save_cover(cover, directory, song_name)    
    
    async with aiofiles.open(song_path, 'wb+') as file_object:
        await file_object.write(await song.read())

    return {'song_path': song_path, 'cover_path': cover_path}


async def save_album_song(song: UploadFile, directory: str) -> dict:
    song_name, song_format = song.filename.split('.')
    song_path = f'{directory}/{song_name}.{song_format}'

    async with aiofiles.open(song_path, 'wb+') as file_object:
        await file_object.write(await song.read())

    return {'path': song_path, 'name': song_name}


def validate_release_date(date):
    """
    Валидация даты релиза
    """
    try:
        if len(date) == 10:  # Формат YYYY-MM-DD
            release_date_dt = datetime.fromisoformat(date + "T00:00")
        elif len(date) == 16:  # Формат YYYY-MM-DDTHH:MM
            release_date_dt = datetime.fromisoformat(date)
        else:
            raise ValueError("Дата релиза должна быть в формате YYYY-MM-DD или YYYY-MM-DDTHH:MM.")

        release_date_dt = datetime.fromisoformat(date)
        if release_date_dt.tzinfo is not None:
            raise ValueError("Дата релиза должна быть наивной (без часового пояса).")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Неверный формат даты: {e}")
    
    return release_date_dt


def validate_song_format(song: str):
    if song.split('.')[-1] != 'mp3':
        raise HTTPException(
            status_code=400,
            detail='Неверный формат файла. Нужен mp3!'
        )
    

def get_directory_name(name: str, username: str, id: int | str = None):
    return datetime.now().strftime(f'uploads/songs/%Y-%m-%d/{username}/{name}')


def get_file_format(file):
    return file.filename.split('.')[-1]