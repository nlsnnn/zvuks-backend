from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import PullBasedJetStreamBroker
from taskiq_redis import RedisAsyncResultBackend, RedisScheduleSource
from app.config import get_redis_url, get_nats_url

redis_url = get_redis_url()
nats_url = get_nats_url()

broker = PullBasedJetStreamBroker(
    servers=nats_url, queue="music_tasks", stream_name="music_stream"
).with_result_backend(RedisAsyncResultBackend(redis_url=redis_url))

label_source = LabelScheduleSource(broker)
redis_source = RedisScheduleSource(redis_url)

scheduler = TaskiqScheduler(broker=broker, sources=[label_source, redis_url])

import app.tasks.music  # noqa
