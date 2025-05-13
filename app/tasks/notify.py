from app.music.models import Album, Song
from app.services.nats_kv import NatsKVService
from app.tq import broker
from app.users.dao import ArtistSubscriberDAO, UsersDAO
from app.email.service import EmailService


nats_kv = NatsKVService()


@broker.task
async def notify_release(
    artist_id: int, release_type: str, release: Song | Album
) -> None:
    subs = await ArtistSubscriberDAO.find_all(artist_id=artist_id)
    for sub in subs:
        await send_single_notification.kiq(
            user_id=sub.subscriber_id,
            artist_id=artist_id,
            release_type=release_type,
            release=release,
        )


@broker.task
async def send_single_notification(
    user_id: int,
    artist_id: int,
    release_type: str,
    release: Song | Album,
) -> None:
    key = f"{release_type}:{release.id}:{user_id}"
    if not await nats_kv.mark_if_new(key):
        return

    user = await UsersDAO.find_one_or_none_by_id(user_id)
    artist = await UsersDAO.find_one_or_none_by_id(artist_id)
    await EmailService.send_release_notification(
        user=user,
        artist_username=artist.username,
        release_type=release_type,
        release_link=f"https://127.0.0.1/profile/{artist_id}",
        release_image=release.cover_path,
    )
