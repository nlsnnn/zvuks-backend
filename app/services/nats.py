from loguru import logger
from nats.js import JetStreamContext

from app.chat.schemas import MessagePublish
from app.config import settings


class NatsService:
    @staticmethod
    async def publish_message_ai(js: JetStreamContext, message_data: MessagePublish):
        try:
            await js.publish(
                subject=settings.message_ai.subject,
                payload=message_data.text.encode(),
                headers={
                    "Message-Id": str(message_data.message_id),
                    "Message-UserId": str(message_data.user_id),
                },
            )

            logger.info(
                f"Message {message_data.message_id} published in subject `{settings.message_ai.subject}`"
            )
        except Exception as e:
            logger.error(f"Error when publishing NATS: {e}")
            raise e
