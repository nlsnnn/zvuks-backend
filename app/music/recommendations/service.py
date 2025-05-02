from app.exceptions import NotFoundException
from app.music.recommendations.dao import RecommendationsDAO
from app.music.service import MusicService
from app.music.song.dao import SongDAO


class RecommendationsService:
    @staticmethod
    async def popular_songs(user_id: int | None = None, limit: int = 10):
        song_ids = await RecommendationsDAO.top_by_plays()
        songs = await SongDAO.find_all_by_ids(song_ids)
        return await MusicService.get_songs_dto(songs, user_id)

    @staticmethod
    async def add_listen(song_id: int, user_id: int):
        song = await SongDAO.find_one_or_none_by_id(song_id)
        if not song:
            raise NotFoundException
        await RecommendationsDAO.add_listen(song_id=song_id, user_id=user_id)

    @staticmethod
    async def get_new_songs(user_id: int | None = None, limit: int = 10):
        songs = await SongDAO.get_latest(limit)
        return await MusicService.get_songs_dto(songs, user_id)
