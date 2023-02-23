from functools import cache

from pydantic import BaseSettings, Field, RedisDsn


class RedisSettings(BaseSettings):
    class Config:
        env_prefix = "REDIS_"

    DSN: RedisDsn = Field("redis://localhost")


@cache
def get_redis_settings() -> RedisSettings:
    """Get cached version of Redis settings."""
    return RedisSettings()
