from functools import cache

from pydantic import BaseSettings, RedisDsn


class RedisSettings(BaseSettings):
    class Config:
        env_prefix = "REDIS_"

    DSN: RedisDsn | None


@cache
def get_redis_settings() -> RedisSettings:
    """Get cached version of Redis settings."""
    return RedisSettings()
