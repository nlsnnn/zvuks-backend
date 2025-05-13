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
    async def add_song(song_data: SongCreate, user_data: User):
        name = song_data.name

        directory = MusicUtils.get_directory_name("songs", name, user_data)
        cover_path = await MusicService.upload_file(
            song_data.cover, directory, ["jpg", "jpeg", "png"]
        )
        song_path = await MusicService.upload_file(
            song_data.song, directory, ["mp3", "wav"]
        )

        artists = await UsersDAO.find_all_by_ids(song_data.artist_ids)

        song_orm = await SongDAO.add(
            name=name,
            path=song_path,
            cover_path=cover_path,
            release_date=song_data.release_date,
            user_id=user_data.id,
            artists=artists,
        )

        if song_data.notify_subscribers:
            await notify_release.kiq(
                artist_id=user_data.id,
                release_type="song",
                release=song_orm,
            )

        return song_orm

    @staticmethod
    async def update_song(song_id: int, song_data: SongUpdate, user: User):
        song = await SongDAO.find_one_or_none_by_id(song_id)
        if not song:
            raise ValueError("Песня не найдена")
        if song.user_id != user.id:
            raise ValueError("Нет прав на редактирование этой песни")
        await SongDAO.update(
            filter_by={"id": song_id}, **song_data.model_dump(exclude_none=True)
        )
