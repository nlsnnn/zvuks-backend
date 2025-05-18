from loguru import logger
from app.services.nats_kv import NatsKVService
from app.tq import broker
from app.users.dao import ArtistSubscriberDAO, UsersDAO
from app.email.service import EmailService

nats_kv = NatsKVService()


@broker.task(retry_on_error=True)
async def notify_release(
    artist_id: int, release_type: str, release_id: int, release_cover: str
) -> None:
    logger.info(f"Старт рассылки для релиза '{release_id}'")
    subs = await ArtistSubscriberDAO.find_all(artist_id=artist_id)
    logger.info(
        f"Кол-во подписчиков для рассылки: {len(subs)} (Release ID: {release_id})"
    )
    for sub in subs:
        await send_single_notification.kiq(
            user_id=sub.subscriber_id,
            artist_id=artist_id,
            release_type=release_type,
            release_id=release_id,
            release_cover=release_cover,
        )


@broker.task
async def send_single_notification(
    user_id: int,
    artist_id: int,
    release_type: str,
    release_id: int,
    release_cover: str,
) -> None:
    key = f"{release_type}:{release_id}:{user_id}"
    if not await nats_kv.mark_if_new(key):
        return

    user = await UsersDAO.find_one_or_none_by_id(user_id)
    artist = await UsersDAO.find_one_or_none_by_id(artist_id)
    try:
        await EmailService.send_release_notification(
            user=user,
            artist_username=artist.username,
            release_type=release_type,
            release_link=f"https://127.0.0.1:5173/profile/{artist_id}",
            release_image=release_cover,
        )
        logger.info(
            f"Успешно отправлено письмо юзеру {user_id} о релизе '{release_id}' от {artist.username}"
        )
    except Exception as e:
        logger.error(
            f"Не удалось отправить письмо юзеру {user_id} о релизе '{release_id}'. Ошибка: {e}"
        )
        return False
