from nats.js.errors import KeyValueError
from app.connections.nats import NatsClient
from app.config import settings


class NatsKVService:
    def __init__(self):
        self._bucket = None

    async def _ensure_bucket(self):
        if self._bucket is None:
            js = await NatsClient.get_jetstream()
            self._bucket = await js.key_value(settings.nats_bucket)
        return self._bucket

    async def mark_if_new(self, key: str, ttl_seconds: int = 7 * 24 * 3600) -> bool:
        """
        Возвращает True, если ключ создан первый раз.
        При повторной попытке возвращает False.
        """
        bucket = await self._ensure_bucket()
        try:
            await bucket.create(key, b"1")
            return True
        except KeyValueError:
            return False
