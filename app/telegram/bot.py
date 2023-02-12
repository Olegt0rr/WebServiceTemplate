import logging

from aiogram import Bot

from .settings import get_telegram_settings

logger = logging.getLogger(__name__)


def create_bot() -> Bot:
    """Create Telegram Bot API client."""
    settings = get_telegram_settings()
    bot = Bot(
        token=settings.TOKEN.get_secret_value(),
        parse_mode="HTML",
    )
    logger.debug("Bot %r created.", bot)
    return bot
