from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from app.config import get_redis_url

redis_url = get_redis_url()

broker = ListQueueBroker(url=redis_url).with_result_backend(
    RedisAsyncResultBackend(redis_url=redis_url)
)
