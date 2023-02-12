import logging
from typing import TYPE_CHECKING

import redis
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from redis.asyncio.retry import Retry
from redis.backoff import FullJitterBackoff

from app.redis.settings import get_redis_settings

from .settings import get_telegram_settings

if TYPE_CHECKING:
    from aiogram.fsm.storage.base import BaseStorage

logger = logging.getLogger(__name__)


def create_storage() -> BaseStorage:
    """Prepare storage for FSM and data bucket."""
    redis_settings = get_redis_settings()
    if redis_settings.DSN is None:
        return MemoryStorage()

    # thanks for https://github.com/sshishov :
    # https://github.com/redis/redis-py/issues/1186#issuecomment-1093799467
    connection_kwargs = {
        "health_check_interval": 30,
        "retry_on_timeout": True,
        "retry_on_error": [
            redis.exceptions.ConnectionError,
            redis.exceptions.TimeoutError,
        ],
        "retry": Retry(
            backoff=FullJitterBackoff(cap=3.0, base=0.1),
            retries=3,
        ),
    }

    telegram_settings = get_telegram_settings()
    storage = RedisStorage.from_url(
        redis_settings.DSN,
        key_builder=DefaultKeyBuilder(),
        state_ttl=telegram_settings.STATE_TTL,
        data_ttl=telegram_settings.STATE_TTL,
        connection_kwargs=connection_kwargs,
    )

    logger.debug("Storage %r created", storage)
    return storage
