from app.music.album.dao import AlbumDAO
from app.music.artist.schemas import AlbumStatsRead, DashboardRead, SongStatsRead
from app.music.favorite.dao import FavoriteAlbumDAO, FavoriteSongDAO
from app.music.service import MusicService
from app.music.song.dao import SongDAO
from app.users.models import User
from app.users.schemas import SUserRead


class ArtistService:
    @staticmethod
    async def get_my_songs(user: User):
        songs = await SongDAO.find_all(user_id=user.id)
        return await MusicService.get_songs_dto(songs)

    @staticmethod
    async def get_my_albums(user: User):
        albums = await AlbumDAO.find_all(user_id=user.id)
        return MusicService.get_albums_dto(albums, [])

    @staticmethod
    async def get_song_stats(song_id: int, user: User):
        song = await SongDAO.find_one_or_none_by_id(song_id)
        if not song:
            raise ValueError("Песня не найдена")
        if song.user_id != user.id:
            raise ValueError("Недостаточно прав")
        artists = [
            SUserRead(id=artist.id, username=artist.username, avatar=artist.avatar_path)
            for artist in song.artists
        ]

        listens = await SongDAO.get_listens_count(song_id)
        favorites = len(await FavoriteSongDAO.find_all(song_id=song_id))
        return SongStatsRead(
            id=song.id,
            name=song.name,
            path=song.path,
            cover_path=song.cover_path,
            release_date=song.release_date,
            is_archive=song.is_archive,
            is_favorite=True,
            artists=artists,
            favortes=favorites,
            listens=listens,
        )

    @staticmethod
    async def get_album_stats(album_id: int, user: User):
        album = await AlbumDAO.find_one_or_none_by_id(album_id)
        if not album:
            raise ValueError("Альбом не найден")
        if album.user_id != user.id:
            raise ValueError("Недостаточно прав")

        artist = SUserRead(
            id=album.user.id,
            username=album.user.username,
            avatar=album.user.avatar_path,
        )
        listens = await ArtistService._get_album_listens_count(album_id)
        favorites = len(await FavoriteAlbumDAO.find_all(album_id=album_id))

        return AlbumStatsRead(
            id=album.id,
            name=album.name,
            cover_path=album.cover_path,
            release_date=album.release_date,
            favorite=True,
            artist=artist,
            favorites=favorites,
            listens=listens,
        )

    @staticmethod
    async def get_dashboard(user: User):
        songs = await SongDAO.find_all(user_id=user.id)
        albums = await AlbumDAO.find_all(user_id=user.id)
        song_ids = [s.id for s in songs]
        album_ids = [a.id for a in albums]
        listens = await SongDAO.get_listens_count_for_songs(song_ids)
        favorite_songs = await FavoriteSongDAO.get_all_by_song_ids(song_ids)
        favorite_albums = await FavoriteAlbumDAO.get_all_by_album_ids(album_ids)

        return DashboardRead(
            listens=listens,
            subscribers=len(user.subscribers),
            songs=len(songs),
            albums=len(albums),
            favorite_songs=len(favorite_songs),
            favorite_albums=len(favorite_albums),
        )

    @staticmethod
    async def _get_album_listens_count(album_id: int):
        songs = await SongDAO.find_all(album_id=album_id)
        song_ids = [song.id for song in songs]
        listens = await SongDAO.get_listens_count_for_songs(song_ids)
        return listens
