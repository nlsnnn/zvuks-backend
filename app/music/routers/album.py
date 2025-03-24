from fastapi import APIRouter, Depends

from app.music.schemas import AlbumCreate
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
    album_data: AlbumCreate = Depends(),
    user_data: User = Depends(token_depends.get_current_user)
) -> dict:
    # date = MusicUtils.validate_release_date(release_date)
    
    name = album_data.name
    directory = MusicUtils.get_directory_name('albums', name, user_data)
    cover_path = await MusicService.upload_file(
        album_data.cover, 
        directory,
        ['jpg', 'jpeg', 'png']
    )
    album = await MusicService.create_album(
        name, 
        cover_path, 
        album_data.release_date, 
        user_data.id
    )

    data = await MusicService.save_album_songs(
        album_data.songs, 
        cover_path, 
        album.id, 
        user_data.id, 
        album_data.song_names, 
        directory
    )

    return {
        "album": {
            "id": album.id,
            "name": name,
            "release_date": album_data.release_date,
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