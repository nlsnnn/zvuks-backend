import asyncio
from fastapi import HTTPException, Request, UploadFile, status

from app.exceptions import AlreadyExistsException, NotFoundException
from app.music.models import Playlist
from app.music.playlist.dao import PlaylistDAO, PlaylistSongDAO
from app.music.playlist.schemas import PlaylistRead, PlaylistCreate, PlaylistSongAdd
from app.music.service import MusicService
from app.music.song.schemas import SongRead
from app.music.utils import MusicUtils
from app.music.song import SongDAO
from app.users.dao import UsersDAO
from app.users.models import User
from app.users.schemas import SUserRead


class PlaylistService:
    @staticmethod
    async def get_all_playlists():
        playlists: list[Playlist] = await PlaylistDAO.find_all()
        # data = []
        # for playlist in playlists:
        #     data.append(await PlaylistService.to_dto(playlist))

        return [await PlaylistService.to_dto(p) for p in playlists]

    @staticmethod
    async def get_playlist(playlist_id: int):
        playlist = await PlaylistDAO.find_one_or_none_by_id(playlist_id)
        if not playlist:
            raise NotFoundException
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
    async def add_playlist_song(data: PlaylistSongAdd):
        exists = await PlaylistSongDAO.find_all(
            **{"playlist_id": data.playlist_id, "song_id": data.song_id}
        )
        if exists:
            raise AlreadyExistsException
        await PlaylistSongDAO.add(playlist_id=data.playlist_id, song_id=data.song_id)

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
