from typing import List
from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.users.dependencies import TokenDepends
from app.music.utils import create_album_directory, save_album_song, save_cover, validate_release_date
from app.music.dao import AlbumDAO, SongDAO
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
    date = validate_release_date(release_date)

    album_directory = await create_album_directory(name, user_data.username)
    cover_path = await save_cover(cover, album_directory, name)

    album_orm = await AlbumDAO.add(
        name=name,
        cover_path=cover_path,
        release_date=date,
        user_id=user_data.id
    )

    songs_added = []
    
    for song in songs:
        song_data = await save_album_song(song, album_directory)

        await SongDAO.add(
            name=song_data['name'],
            path=song_data['path'],
            cover_path=cover_path,
            album_id=album_orm.id
        )

        songs_added.append(song_data)

    return {
        "album": {
            "id": album_orm.id,
            "name": name,
            "release_date": date,
            "songs": songs_added
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