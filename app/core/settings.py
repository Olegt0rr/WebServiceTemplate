from pydantic_settings import BaseSettings, SettingsConfigDict


class WebAppSettings(BaseSettings):
    """Represents settings for web application."""

    model_config = SettingsConfigDict(env_prefix="WEBAPP_")

    HOST: str = "0.0.0.0"  # noqa: S104
    PORT: int = 8080
