from typing import Optional
from fastapi import APIRouter, Depends, HTTPException

from app.music.service import MusicService
from app.users.dependencies import TokenDepends
from app.music.schemas import SongCreate, SongUpdate
from app.music.utils import MusicUtils
from app.music.dao import SongDAO
from app.users.models import User


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
    song_data: SongCreate = Depends(SongCreate.as_form), 
    user_data: User = Depends(token_depends.get_current_user)
) -> dict:
    name = song_data.name

    directory = MusicUtils.get_directory_name('songs', name, user_data)
    cover_path = await MusicService.upload_file(
        song_data.cover, 
        directory,
        ['jpg', 'jpeg', 'png']
    )
    song_path = await MusicService.upload_file(
        song_data.song,
        directory,
        ['mp3', 'wav']
    )

    song_orm = await SongDAO.add(
        name=name,
        path=song_path,
        cover_path=cover_path,
        release_date=song_data.release_date,
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
