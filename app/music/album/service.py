import asyncio
from typing import Optional
from fastapi import HTTPException, UploadFile, status

from app.music.favorite.dao import FavoriteAlbumDAO
from app.music.service import MusicService
from app.music.utils import MusicUtils
from app.music.album import AlbumDAO, AlbumCreate, AlbumRead
from app.music.song import SongDAO
from app.users.dao import UsersDAO
from app.users.models import User
from app.users.schemas import SUserRead


class AlbumService:
    @staticmethod
    async def get_album(id: int, user_id: Optional[int]):
        album = await AlbumDAO.find_one_or_none_by_id(id)
        if not album:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Альбом не найден"
            )
        author = await UsersDAO.find_one_or_none_by_id(album.user_id)
        if user_id:
            favorite = await FavoriteAlbumDAO.find_one_or_none(
                user_id=user_id, album_id=album.id
            )
            is_favorite = True if favorite else False

        data = AlbumRead(
            id=album.id,
            name=album.name,
            release_date=album.release_date,
            cover_path=album.cover_path,
            favorite=False if not user_id else is_favorite,
            artist=SUserRead(
                id=author.id, username=author.username, avatar=author.avatar_path
            ),
        )
        return data

    @staticmethod
    async def get_all_albums(archive: bool = False):
        albums = await AlbumDAO.find_all(is_archive=archive)
        data = MusicService.get_albums_dto(albums)
        return data

    @staticmethod
    async def get_album_songs(album_id: int, user_id: Optional[int]):
        songs = await SongDAO.find_all(album_id=album_id)
        data = await MusicService.get_songs_dto(songs, user_id)
        return data

    @staticmethod
    async def add_album(album_data: AlbumCreate, user_data: User):
        name = album_data.name

        directory = MusicUtils.get_directory_name("albums", name, user_data)
        cover_path = await MusicService.upload_file(
            album_data.cover, directory, ["jpg", "jpeg", "png"]
        )
        album = await AlbumService.create_album(
            name, cover_path, album_data.release_date, user_data.id
        )

        songs = await AlbumService.save_album_songs(
            album_data.songs,
            cover_path,
            album.id,
            user_data.id,
            album_data.song_names,
            album_data.track_numbers,
            album_data.song_artists_ids,
            directory,
        )

        return [album, songs]

    @staticmethod
    async def create_album(name: str, cover_path: str, date: str, user_id: int):
        album = await AlbumDAO.add(
            name=name, cover_path=cover_path, release_date=date, user_id=user_id
        )
        return album

    @staticmethod
    async def save_album_songs(
        songs: list[UploadFile],
        cover_path: str,
        album_id: int,
        user_id: int,
        song_names: list[str],
        track_numbers: list[int],
        song_artists_ids: list[int],
        directory: str,
    ):
        author = await UsersDAO.find_one_or_none_by_id(user_id)
        tasks = []

        for i, song in enumerate(songs):
            tasks.append(
                AlbumService.save_album_song(
                    song,
                    author,
                    cover_path,
                    album_id,
                    song_names[i],
                    track_numbers[i],
                    song_artists_ids[i],
                    directory,
                )
            )

        songs_added = await asyncio.gather(*tasks)

        data = await MusicService.get_songs_dto(songs_added)
        return data

    @staticmethod
    async def save_album_song(
        song: UploadFile,
        author: User,
        cover_path: str,
        album_id: int,
        song_name: str,
        track_number: int,
        song_artists_ids: list[int],
        directory: str,
    ):
        song_path = await MusicService.upload_file(song, directory, ["mp3", "wav"])

        if len(song_artists_ids) < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="В треке должен быть как минимум 1 артист",
            )
        song_artists = await UsersDAO.find_all_by_ids(song_artists_ids)

        song_orm = await SongDAO.add(
            name=song_name,
            track_number=track_number,
            path=song_path,
            cover_path=cover_path,
            album_id=album_id,
            user_id=author.id,
            artists=song_artists,
        )
        return song_orm
