from datetime import datetime, timezone
from app.music.album.dao import AlbumDAO
from app.music.exceptions import (
    SongCreateException,
    SongReadException,
    SongUpdateException,
)
from app.music.song import SongDAO, SongCreate
from app.music.service import MusicService
from app.music.song.schemas import SongUpdate
from app.music.utils import MusicUtils
from app.tasks.notify import notify_release
from app.users.dao import UsersDAO
from app.users.models import User


class SongService:
    @staticmethod
    async def get_songs(archive: bool = False, user_id: int = None):
        songs = await SongDAO.find_all(**{"is_archive": archive})
        data = await MusicService.get_songs_dto(songs, user_id)
        return data

    @staticmethod
    async def get_song(song_id: int, user_id: int = None):
        song = await SongDAO.find_one_or_none_by_id(song_id)
        if not song:
            raise SongReadException(status_code=404, message="Песня не найдена")
        data = await MusicService.get_songs_dto([song], user_id)
        return data[0]

    @staticmethod
    async def search_songs(query: str, user_id: int):
        songs = await SongDAO.search(query.strip())
        return await MusicService.get_songs_dto(songs, user_id)

    @staticmethod
    async def add_song(song_data: SongCreate, user_data: User):
        if not user_data.is_user:
            raise SongCreateException("Нет прав на создание песни", 403)
        name = song_data.name

        directory = MusicUtils.get_directory_name("songs", name, user_data)
        cover_path = await MusicService.upload_file(
            song_data.cover, directory, ["jpg", "jpeg", "png"]
        )
        song_path = await MusicService.upload_file(
            song_data.song, directory, ["mp3", "wav"]
        )

        release_date = song_data.release_date.replace(tzinfo=timezone.utc)
        release_now = release_date <= datetime.now(tz=timezone.utc)

        artists = await UsersDAO.find_all_by_ids(song_data.artist_ids)

        song_orm = await SongDAO.add(
            name=name,
            path=song_path,
            cover_path=cover_path,
            release_date=song_data.release_date,
            user_id=user_data.id,
            artists=artists,
            is_archive=not release_now,
        )


        if song_data.notify_subscribers:
            await notify_release.kiq(
                artist_id=user_data.id,
                release_type="song",
                release_id=song_orm.id,
                release_cover=song_orm.cover_path,
            )

        return song_orm

    @staticmethod
    async def update_song(song_id: int, song_data: SongUpdate, user: User):
        song = await SongDAO.find_one_or_none_by_id(song_id)
        if not song:
            raise SongUpdateException("Песня не найдена", 404)
        if song.user_id != user.id:
            raise SongUpdateException("Нет прав на редактирование этой песни", 403)
        if song_data.album_id:
            album = await AlbumDAO.find_one_or_none_by_id(song_data.album_id)
            if not album:
                raise SongUpdateException("Альбом не найден", 404)
            if album.user_id != user.id:
                raise SongUpdateException(
                    "Нет прав на редактирование этого альбома", 403
                )
        await SongDAO.update(
            filter_by={"id": song_id}, **song_data.model_dump(exclude_none=True)
        )
