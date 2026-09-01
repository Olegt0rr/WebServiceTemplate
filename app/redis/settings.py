from functools import cache

from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    DSN: RedisDsn = RedisDsn("redis://localhost")


@cache
def get_redis_settings() -> RedisSettings:
    """Get cached version of Redis settings."""
    return RedisSettings()
