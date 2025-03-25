from fastapi import APIRouter, Depends

from app.music.album import AlbumDAO, AlbumCreate
from app.music.album.service import AlbumService
from app.users.dependencies import TokenDepends
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
    album, songs = await AlbumService.add_album(album_data, user_data)

    return {
        "album": {
            "id": album.id,
            "name": album_data.name,
            "release_date": album_data.release_date,
            "songs": songs
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