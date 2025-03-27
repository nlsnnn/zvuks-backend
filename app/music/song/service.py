from app.music.song import SongDAO, SongCreate
from app.music.service import MusicService
from app.music.utils import MusicUtils
from app.users.dao import UsersDAO
from app.users.models import User


class SongService:
    @staticmethod
    async def get_songs(archive: bool = False):
        songs = await SongDAO.find_all(**{"is_archive": archive})

        data = await MusicService.get_songs_dto(songs)
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

        artists = await UsersDAO.find_all_users_by_ids(song_data.artist_ids)

        song_orm = await SongDAO.add(
            name=name,
            path=song_path,
            cover_path=cover_path,
            release_date=song_data.release_date,
            user_id=user_data.id,
            artists=artists,
        )

        return song_orm
