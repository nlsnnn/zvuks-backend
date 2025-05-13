from taskiq import TaskiqScheduler
from app.tq import broker
from app.users.dao import ArtistSubscriberDAO
from app.email.service import EmailService


@broker.task
async def notify_release(artist_id: int, release_type: str, release_id: int) -> None:
    subs = await ArtistSubscriberDAO.find_all(artist_id=artist_id)
    for sub in subs:
        await send_single_notification.kiq(
            user_id=sub.subscriber_id,
            artist_id=artist_id,
            release_type=release_type,
            release_id=release_id,
        )


@broker.task
async def send_single_notification(
    user_id: int,
    artist_id: int,
    release_type: str,
    release_id: int,
) -> None:
    key = f"{release_type}:{release_id}:{user_id}"
    # # if not await nats_kv.mark_if_new(key):
    #     return

    # user = await UserDAO.get(user_id)
    # subject = f"Новая {release_type} от артиста {artist_id}"
    # body = f"Привет, {user.name}! Вышла новая {release_type} (ID: {release_id})."
    # await EmailService.send_email(to_email=user.email, subject=subject, body=body)
