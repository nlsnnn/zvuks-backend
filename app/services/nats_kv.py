from nats.js.api import KeyValueConfig
from nats.js.errors import KeyValueError, BucketNotFoundError
from app.connections.nats import NatsClient


class NatsKVService:
    def __init__(self):
        self._bucket = None

    async def _ensure_bucket(self):
        if self._bucket is None:
            self.js = await NatsClient.get_jetstream()
            self._bucket = await self._get_kv("notify")
        return self._bucket

    async def _get_kv(self, bucket: str):
        try:
            return await self.js.key_value("notify")
        except BucketNotFoundError:
            return await self.js.create_key_value(KeyValueConfig(bucket=bucket))

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
