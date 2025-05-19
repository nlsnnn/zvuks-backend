from typing import List
from app.exceptions import NoUserException
from app.music.favorite.dao import FavoriteSongDAO
from app.music.service import MusicService
from app.music.song.dao import SongDAO
from app.services.utils import Utils
from app.users.dao import ArtistSubscriberDAO, UsersDAO
from app.users.models import User
from app.users.schemas import SUserProfile, SUserRead, SUserUpdate


class UserService:
    @staticmethod
    def get_user_dto(user_data: User):
        return SUserRead(
            id=user_data.id, username=user_data.username, avatar=user_data.avatar_path
        )

    @staticmethod
    def get_users_dto(users: List[User]):
        data = [
            SUserRead(id=user.id, username=user.username, avatar=user.avatar_path)
            for user in users
        ]
        return data

    @staticmethod
    def get_me(user: User):
        role = UserService.get_role(user)
        return SUserRead(
            id=user.id, username=user.username, avatar=user.avatar_path, role=role
        )

    @staticmethod
    async def get_profile(user_id: int, current_user: User):
        user = await UsersDAO.find_one_or_none_by_id(user_id)
        if not user:
            raise NoUserException
        favorites = await FavoriteSongDAO.find_all(user_id=user_id)
        favorite_ids = [favorite.song_id for favorite in favorites]
        songs = await SongDAO.find_all_by_ids(favorite_ids)
        songs_dto = await MusicService.get_songs_dto(songs[:5])
        subscribed = await ArtistSubscriberDAO.find_one_or_none(
            subscriber_id=current_user.id, artist_id=user_id
        )
        data = SUserProfile(
            id=user.id,
            username=user.username,
            avatar=user.avatar_path,
            songs=songs_dto,
            bio=user.bio,
            subscribed=True if subscribed else False,
            blocked=not user.is_user,
        )

        return data

    @staticmethod
    async def update_user(data: SUserUpdate, user: User):
        updates = {}
        if data.avatar:
            updates["avatar_path"] = await UserService.save_avatar(data.avatar, user)
        if data.bio:
            updates["bio"] = data.bio
        if updates:
            await UsersDAO.update(filter_by={"id": user.id}, **updates)

        user_updated = await UsersDAO.find_one_or_none_by_id(user.id)
        user_dto = UserService.get_user_dto(user_updated)
        return user_dto

    @staticmethod
    async def subscribe_user(user_id: int, current_user_id: int):
        if user_id == current_user_id:
            raise ValueError("Нельзя подписаться на самого себя")
        exists = await ArtistSubscriberDAO.find_one_or_none(
            artist_id=user_id, subscriber_id=current_user_id
        )
        if exists:
            raise ValueError("Вы уже подписаны на этого исполнителя")
        users = await UsersDAO.find_all_by_ids([user_id, current_user_id])
        if len(users) != 2:
            raise ValueError("Пользователи не найдены")
        await ArtistSubscriberDAO.add(artist_id=user_id, subscriber_id=current_user_id)

    @staticmethod
    async def unsubscribe_user(user_id: int, current_user_id: int):
        exists = await ArtistSubscriberDAO.find_one_or_none(
            artist_id=user_id, subscriber_id=current_user_id
        )
        if not exists:
            raise ValueError("Вы не подписаны на этого исполнителя")
        await ArtistSubscriberDAO.delete(
            artist_id=user_id, subscriber_id=current_user_id
        )

    @staticmethod
    async def save_avatar(file, user: User):
        directory = UserService.get_directory_name(user)
        path = await Utils.upload_file(file, directory, ["png", "jpg", "jpeg"])
        return path

    @staticmethod
    def get_directory_name(user: User):
        return f"avatars/{user.id}"

    @staticmethod
    def get_role(user: User):
        if user.is_admin:
            return "admin"
        if user.is_user:
            return "user"
        return "block"
