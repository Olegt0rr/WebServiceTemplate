import logging
from typing import TYPE_CHECKING

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from app.redis import create_redis, get_redis_settings

from .settings import get_telegram_settings

if TYPE_CHECKING:
    from aiogram.fsm.storage.base import BaseStorage

logger = logging.getLogger(__name__)


def create_storage() -> "BaseStorage":
    """Prepare storage for FSM and data bucket."""
    redis_settings = get_redis_settings()
    if redis_settings.DSN is None:
        return MemoryStorage()

    telegram_settings = get_telegram_settings()
    storage = RedisStorage(
        redis=create_redis(),
        key_builder=DefaultKeyBuilder(),
        state_ttl=telegram_settings.STATE_TTL,
        data_ttl=telegram_settings.STATE_TTL,
    )

    logger.debug("Storage %r created", storage)
    return storage
