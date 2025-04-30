from app.exceptions import AlreadyExistsException, ForbiddenException, NotFoundException
from app.music.models import Playlist
from app.music.playlist.dao import PlaylistDAO, PlaylistSongDAO
from app.music.playlist.schemas import (
    PlaylistRead,
    PlaylistCreate,
    PlaylistSongAdd,
    PlaylistUpdate,
)
from app.music.service import MusicService
from app.music.utils import MusicUtils
from app.music.song import SongDAO
from app.users.models import User
from app.users.schemas import SUserRead


class PlaylistService:
    @staticmethod
    async def get_all_playlists():
        playlists: list[Playlist] = await PlaylistDAO.find_all()

        return [await PlaylistService.to_dto(p) for p in playlists]

    @staticmethod
    async def get_user_playlists(user_id: int, user_data: User):
        if user_id == user_data.id:
            playlists = await PlaylistDAO.find_all(user_id=user_id)
        else:
            playlists = await PlaylistDAO.find_all(user_id=user_id, private=False)

        return [await PlaylistService.to_dto(p) for p in playlists]

    @staticmethod
    async def get_playlist(playlist_id: int):
        playlist = await PlaylistService._is_exists(playlist_id)
        return await PlaylistService.to_dto(playlist)

    @staticmethod
    async def create_playlist(data: PlaylistCreate, user: User):
        directory = MusicUtils.get_directory_name("playlists", data.name, user)
        cover_path = await MusicService.upload_file(
            data.cover, directory, ["jpg", "jpeg", "png"]
        )
        playlist = await PlaylistDAO.add(
            name=data.name, cover_path=cover_path, private=data.private, user_id=user.id
        )
        return playlist

    @staticmethod
    async def delete_playlist(playlist_id: int, user: User):
        await PlaylistService._is_exists(playlist_id)
        await PlaylistService._is_author(playlist_id, user)

        await PlaylistDAO.delete(id=playlist_id)

    @staticmethod
    async def update_playlist(playlist_id: int, data: PlaylistUpdate, user: User):
        playlist = await PlaylistService._is_exists(playlist_id)
        await PlaylistService._is_author(playlist_id, user)

        updates = {}
        if data.name is not None:
            updates["name"] = data.name
        if data.private is not None:
            updates["private"] = data.private
        if data.cover is not None:
            name = updates.get("name", playlist.name)
            directory = MusicUtils.get_directory_name("playlists", name, user)
            cover_path = await MusicService.upload_file(
                data.cover, directory, ["jpg", "jpeg", "png"]
            )
            updates["cover_path"] = cover_path

        if updates:
            await PlaylistDAO.update(filter_by={"id": playlist_id}, **updates)

    @staticmethod
    async def add_playlist_song(data: PlaylistSongAdd):
        exists = await PlaylistSongDAO.find_all(
            **{"playlist_id": data.playlist_id, "song_id": data.song_id}
        )
        if exists:
            raise AlreadyExistsException
        song = await SongDAO.find_one_or_none_by_id(data.song_id)
        playlist = await PlaylistDAO.find_one_or_none_by_id(data.playlist_id)
        if not song or not playlist:
            raise NotFoundException
        await PlaylistSongDAO.add(playlist_id=data.playlist_id, song_id=data.song_id)

    @staticmethod
    async def delete_playlist_song(data: PlaylistSongAdd, user: User):
        await PlaylistService._is_exists(data.playlist_id)
        await PlaylistService._is_author(data.playlist_id, user)

        await PlaylistSongDAO.delete(playlist_id=data.playlist_id, song_id=data.song_id)

    @staticmethod
    async def to_dto(playlist: Playlist):
        user = playlist.user
        songs = await MusicService.get_songs_dto(playlist.songs)
        author = SUserRead(
            id=user.id,
            username=user.username,
            avatar=user.avatar_path,
        )
        return PlaylistRead(
            name=playlist.name,
            cover=playlist.cover_path,
            private=playlist.private,
            author=author,
            songs=songs,
        )

    @staticmethod
    async def _is_author(playlist_id: int, user: User):
        playlist = await PlaylistDAO.find_one_or_none_by_id(playlist_id)
        if playlist.user_id != user.id:
            raise ForbiddenException
        return playlist

    @staticmethod
    async def _is_exists(playlist_id: int):
        playlist = await PlaylistDAO.find_one_or_none_by_id(playlist_id)
        if not playlist:
            raise NotFoundException
        return playlist
