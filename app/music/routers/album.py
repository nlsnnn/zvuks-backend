from typing import List
from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.config import get_s3_base_url
from app.music.service import MusicService
from app.users.dependencies import TokenDepends
from app.music.utils import MusicUtils
from app.music.dao import AlbumDAO
from app.users.models import User


router = APIRouter(prefix='/album', tags=['Album'])

token_depends = TokenDepends()


@router.get('/')
async def get_all_albums():
    albums = await AlbumDAO.find_all()
    print(f'{albums=}')
    return {'albums': albums}


@router.get('/{album_id}/')
async def get_album(album_id: int):
    album = await AlbumDAO.find_one_or_none_by_id(album_id)
    return {'album': album}


@router.post('/')
async def add_album(
    name: str = Form(description='Название альбома'),
    release_date: str = Form(description='Дата релиза альбома (YYYY-MM-DDTHH:MM)'),
    cover: UploadFile = File(description='Обложка альбома'),
    songs: List[UploadFile] = File(description='Файлы песен'),
    user_data: User = Depends(token_depends.get_current_user)
) -> dict:
    date = MusicUtils.validate_release_date(release_date)
    
    directory = MusicUtils.get_album_directory_name(name, user_data.username, user_data.id)
    cover_path = await MusicService.upload_cover(cover, name, directory)
    absolute_cover_path = get_s3_base_url() + "/" + cover_path
    album = await MusicService.create_album(name, absolute_cover_path, date, user_data.id)

    data = await MusicService.save_album_songs(
        songs, 
        absolute_cover_path, 
        album.id, 
        user_data.id, 
        name, 
        directory
    )

    return {
        "album": {
            "id": album.id,
            "name": name,
            "release_date": date,
            "songs": data
        }
    }


@router.patch('/{album_id}')
async def update_album(album_id: int):
    album = await AlbumDAO.find_one_or_none_by_id(album_id)
    return {'message': 'ok'}


@router.delete('/{album_id}')
async def delete_album(album_id: int):
    await AlbumDAO.delete(id=album_id)
    return {'message': f'Album {album_id} successfull deleted!'}