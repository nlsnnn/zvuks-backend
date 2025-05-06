from app.music.song.dao import SongDAO
from app.tq import broker


@broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def scan_and_publish_song():
    songs = await SongDAO.get_to_publish()
    for song in songs:
        await SongDAO.update(filter_by={"id": song.id}, is_archive=False)