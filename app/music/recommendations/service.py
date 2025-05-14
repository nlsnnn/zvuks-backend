from app.exceptions import NotFoundException
from app.music.recommendations.dao import RecommendationsDAO
from app.music.service import MusicService
from app.music.song.dao import SongDAO


class RecommendationsService:
    @staticmethod
    async def popular_songs(user_id: int | None = None, limit: int = 10):
        song_ids = await RecommendationsDAO.top_by_plays(limit=limit)
        songs = await SongDAO.find_all_by_ids(song_ids, is_archive=False)
        return await MusicService.get_songs_dto(songs, user_id)

    @staticmethod
    async def add_listen(song_id: int, user_id: int):
        song = await SongDAO.find_one_or_none_by_id(song_id)
        if not song:
            raise NotFoundException
        await RecommendationsDAO.add_listen(song_id=song_id, user_id=user_id)

    @staticmethod
    async def get_new_songs(user_id: int | None = None, days: int = 7, limit: int = 10):
        songs = await SongDAO.get_latest(days=days, limit=limit)
        seen_song_ids = {song.id for song in songs}
        max_days = 21

        while len(songs) < limit:
            days *= 2
            if days > max_days:
                break
            additional_songs = await SongDAO.get_latest(
                days=days, limit=limit - len(songs)
            )
            if not additional_songs:
                break
            for song in additional_songs:
                if song.id not in seen_song_ids:
                    songs.append(song)
                    seen_song_ids.add(song.id)

        return await MusicService.get_songs_dto(songs[:limit], user_id)

    @staticmethod
    async def get_favorites_songs(user_id: int, limit: int = 10):
        song_ids = await RecommendationsDAO.get_favorites_songs(days=7, limit=limit)
        songs = await SongDAO.find_all_by_ids(song_ids, is_archive=False)
        return await MusicService.get_songs_dto(songs, user_id)
