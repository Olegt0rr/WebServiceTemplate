from __future__ import annotations

from typing import TYPE_CHECKING

from .client import create_redis

if TYPE_CHECKING:
    from aiohttp.web_app import Application

    from redis.asyncio import Redis

REDIS_APP = "redis"


def setup_redis(app: Application) -> None:
    """Set up Redis client."""
    app[REDIS_APP] = create_redis()
    app.on_shutdown.append(close_redis)


async def close_redis(app: Application) -> None:
    """Graceful Redis client close."""
    redis: Redis = app[REDIS_APP]
    await redis.close()
