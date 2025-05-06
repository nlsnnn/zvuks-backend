from app.music.song.dao import SongDAO
from app.tq import broker


@broker.task(schedule_time=...)
async def publish_song(song_id: int):
    await SongDAO.update(filter_by={"id": song_id}, is_archive=False)
