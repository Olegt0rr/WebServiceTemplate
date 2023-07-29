import logging

import redis
from redis.asyncio import Redis
from redis.asyncio.retry import Retry
from redis.backoff import FullJitterBackoff

from .settings import get_redis_settings

logger = logging.getLogger(__name__)


def create_redis() -> Redis:
    """Create Redis client.

    Thanks https://github.com/sshishov for connection kwargs:
    https://github.com/redis/redis-py/issues/1186#issuecomment-1093799467
    """
    redis_settings = get_redis_settings()
    client = Redis.from_url(
        url=str(redis_settings.DSN),
        decode_responses=True,
        health_check_interval=30,
        retry_on_timeout=True,
        retry_on_error=[
            redis.exceptions.ConnectionError,
            redis.exceptions.TimeoutError,
        ],
        retry=Retry(
            backoff=FullJitterBackoff(cap=3.0, base=0.1),
            retries=3,
        ),
    )
    logger.debug("Redis %r created.", client)
    return client
