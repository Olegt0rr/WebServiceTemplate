import logging

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

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


async def bot_is_available(bot: Bot) -> bool:
    """Check Telegram Bot API is available for bot."""
    try:
        await bot.get_me()
    except TelegramAPIError:
        return False
    return True
