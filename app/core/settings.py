from pydantic import BaseSettings


class WebAppSettings(BaseSettings):
    """Represents settings for web application."""

    class Config:
        env_prefix = "WEBAPP_"

    HOST: str = "0.0.0.0"  # noqa: S104
    PORT: int = 8080
