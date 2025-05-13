import nats
from nats.js import JetStreamContext
from app.config import get_nats_url


class NatsClient:
    _nc = None
    _js: JetStreamContext = None

    @classmethod
    async def get_connection(cls):
        if cls._nc is None or cls._nc.is_closed:
            cls._nc = await nats.connect(
                servers=get_nats_url(),
            )
        return cls._nc

    @classmethod
    async def get_jetstream(cls) -> JetStreamContext:
        if cls._js is None:
            nc = await cls.get_connection()
            cls._js = nc.jetstream()
        return cls._js
