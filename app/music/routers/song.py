from typing import Optional
from aiohttp import ClientError
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.music.service import MusicService
from app.users.dependencies import TokenDepends
from app.music.schemas import SongRead, SongUpdate
from app.music.utils import get_directory_name, save_song, validate_release_date
from app.music.dao import SongDAO
from app.users.models import User
from app.config import settings


router = APIRouter(prefix='/song', tags=['Song'])

token_depends = TokenDepends()

@router.get('/')
async def get_all_songs(archive: Optional[bool] = False):
    data = await MusicService.get_songs(archive)
    return {'songs': data}


@router.get('/{song_id}/')
async def get_song(song_id: int):
    song = await SongDAO.find_one_or_none_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    return {'song_path': song.path, 'cover_path': song.cover_path}


@router.post("/")
async def add_song(
  name: str = Form(description='Название песни'),
  release_date: str = Form(description='Дата релиза песни (YYYY-MM-DDTHH:MM)'),
  song: UploadFile = File(description='Файл песни'),
  cover: UploadFile = File(description='Обложка песни'),
  user_data: User = Depends(token_depends.get_current_user)
) -> dict:
    release_date_dt = validate_release_date(release_date)

    directory = get_directory_name(name, user_data.username, user_data.id)
    cover_path = await MusicService.upload_cover(cover, name, directory)
    song_path = await MusicService.save_song(song, name, directory)

    song_path = settings.s3.endpoint + "/" + settings.s3.bucket_name + "/" + song_path
    cover_path = settings.s3.endpoint + "/" + settings.s3.bucket_name + "/" + cover_path

    song_orm = await SongDAO.add(
        name=name,
        path=song_path,
        cover_path=cover_path,
        release_date=release_date_dt,
        user_id=user_data.id
    )

    return {"id": song_orm.id, "name": name, 'path': song_path, 'cover_path': cover_path}


@router.put('/{song_id}/')
async def update_song(song_id: int, data: SongUpdate):
    song = await SongDAO.find_one_or_none_by_id(song_id)
    return {'ok': 'ok'}


@router.delete('/{song_id}/')
async def delete_song(song_id: int):
    await SongDAO.delete(id=song_id)
    return {'message': f'Song {song_id} successfull deleted!'}
