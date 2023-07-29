from functools import cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramSettings(BaseSettings):
    """Represents Telegram settings."""

    model_config = SettingsConfigDict(env_prefix="TELEGRAM_")

    TOKEN: SecretStr
    SKIP_UPDATES: bool = False
    STATE_TTL: int = 60 * 60 * 24 * 30  # 1 month
    DATA_TTL: int = 60 * 60 * 24 * 30  # 1 month
    WEBHOOK_ENABLED: bool = False
    WEBHOOK_PATH: str = "/webhook"

    @property
    def bot_id(self) -> int:
        """Parse bot id from token."""
        raw_bot_id, *_ = self.TOKEN.get_secret_value().split(":")
        return int(raw_bot_id)


@cache
def get_telegram_settings() -> TelegramSettings:
    """Get cached version of settings."""
    return TelegramSettings()
