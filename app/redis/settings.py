from functools import cache

from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    DSN: RedisDsn = Field("redis://localhost")


@cache
def get_redis_settings() -> RedisSettings:
    """Get cached version of Redis settings."""
    return RedisSettings()
