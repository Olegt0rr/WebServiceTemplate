from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from .settings import get_telegram_settings

if TYPE_CHECKING:
    from aiogram.fsm.storage.base import BaseStorage
    from redis.asyncio import Redis

logger = logging.getLogger(__name__)


def create_storage(redis: Redis | None = None) -> BaseStorage:
    """Prepare storage for FSM and data bucket."""
    if redis is None:
        return MemoryStorage()

    telegram_settings = get_telegram_settings()
    storage = RedisStorage(
        redis=redis,
        key_builder=DefaultKeyBuilder(),
        state_ttl=telegram_settings.STATE_TTL,
        data_ttl=telegram_settings.STATE_TTL,
    )

    logger.debug("Storage %r created", storage)
    return storage
