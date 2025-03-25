import uuid
from fastapi import HTTPException, UploadFile

from app.config import get_s3_base_url, get_s3_client
from app.music.album.dao import AlbumDAO
from app.music.models import Song
from app.music.song import SongRead
from app.music.utils import MusicUtils
from app.users.dao import UsersDAO


class MusicService:
    @staticmethod
    async def get_songs_dto(songs: list[Song]):
        user_ids = await MusicService._get_user_ids(songs)

        users = await UsersDAO.find_all_users_by_ids(list(user_ids))
        user_dict = {user.id: user for user in users}

        data = []
        for song in songs:
            author = user_dict.get(song.user_id)
            if not author and song.album_id:
                album = await AlbumDAO.find_one_or_none_by_id(song.album_id)
                author = user_dict.get(album.user_id)
                continue
            
            data.append(SongRead(
                id=song.id,
                name=song.name,
                path=song.path,
                cover_path=song.cover_path,
                release_date=song.release_date,
                is_archive=song.is_archive,
                author=author.username if author else "Unknown"
            ))
        return data
    

    @staticmethod
    async def _get_user_ids(songs: list[Song]):
        user_ids = set()
        album_ids = set()

        for song in songs:
            if song.user_id:
                user_ids.add(song.user_id)
            else:
                album_ids.add(song.album_id)
        
        if album_ids:
            albums = await AlbumDAO.find_all(id=album_ids)
            user_ids.update(album.user_id for album in albums)
        
        return user_ids      


    @staticmethod
    async def upload_file(file: UploadFile, directory: str, allowed_formats: list[str]):
        file_format = MusicUtils.get_file_format(file)
        if file_format not in allowed_formats:
            return HTTPException(400, f"Недопустимый формат файла: {file_format}")
        
        file_content = await file.read()
        filename = f"{uuid.uuid4()}/{file_format}"
        path = f"{directory}/{filename}"

        s3_client = get_s3_client()
        await s3_client.upload_file(file_content, path)
        return f"{get_s3_base_url()}/{path}"