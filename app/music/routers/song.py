from aiohttp import ClientError
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.music.service import MusicService
from app.users.dependencies import TokenDepends
from app.music.schemas import SongUpdate
from app.music.utils import save_song, validate_release_date
from app.music.dao import SongDAO
from app.users.models import User


router = APIRouter(prefix='/song', tags=['Song'])

token_depends = TokenDepends()

@router.get('/')
async def get_all_songs():
    songs = await SongDAO.find_all()
    return {'songs': songs}


@router.get('/{song_id}/')
async def get_song(song_id: int):
    song = await SongDAO.find_one_or_none_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    try:
        file = await MusicService.get_song(song.path)
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving file from S3: {e}")

    async def stream_file():
        try:
            async for chunk in file['Body'].iter_chunks():
                yield chunk
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error streaming file: {e}")

    return StreamingResponse(
        stream_file(),
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": f"attachment; filename={song.name}"
        }
    )



@router.post("/")
async def add_song(
  name: str = Form(description='Название песни'),
  release_date: str = Form(description='Дата релиза песни (YYYY-MM-DDTHH:MM)'),
  song: UploadFile = File(description='Файл песни'),
  cover: UploadFile = File(description='Обложка песни'),
  user_data: User = Depends(token_depends.get_current_user)
) -> dict:
    release_date_dt = validate_release_date(release_date)

    # song_data = await save_song(song, cover, name, user_data.username)
    song_data = await MusicService.save_song(song, cover, name, user_data.username)
    duration = MusicService.get_audio_duration(song)

    await SongDAO.add(
        name=name,
        path=song_data['song_path'],
        cover_path=song_data['cover_path'],
        release_date=release_date_dt,
        user_id=user_data.id
    )

    return {"name": name, "data": song_data}


@router.put('/{song_id}/')
async def update_song(song_id: int, data: SongUpdate):
    song = await SongDAO.find_one_or_none_by_id(song_id)
    return {'ok': 'ok'}


@router.delete('/{song_id}/')
async def delete_song(song_id: int):
    await SongDAO.delete(id=song_id)
    return {'message': f'Song {song_id} successfull deleted!'}
