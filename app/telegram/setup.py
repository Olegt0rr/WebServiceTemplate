from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from .bot import create_bot
from .dispatcher import create_dispatcher
from .settings import get_telegram_settings
from .storage import create_storage

if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher
    from aiogram.fsm.storage.base import BaseStorage
    from aiohttp.web_app import Application


def setup_telegram(app: Application) -> None:
    """Set up app for receiving Telegram updates."""
    settings = get_telegram_settings()

    bot = app["bot"] = create_bot()
    redis = app.get("redis")
    storage = app["storage"] = create_storage(redis)
    dispatcher = app["dispatcher"] = create_dispatcher(storage)

    if settings.WEBHOOK_ENABLED:
        handler = SimpleRequestHandler(dispatcher=dispatcher, bot=bot)
        handler.register(app, path=settings.WEBHOOK_PATH)
    else:
        app.on_startup.append(start_polling)
        app.on_shutdown.append(stop_polling)

    app.on_shutdown.append(close_storage)


async def start_polling(app: Application) -> None:
    """Start Telegram polling on app startup."""
    dispatcher: Dispatcher = app["dispatcher"]
    bot: Bot = app["bot"]
    polling_coroutine = dispatcher.start_polling(bot)
    app["polling_task"] = asyncio.create_task(polling_coroutine)


async def stop_polling(app: Application) -> None:
    """Stop Telegram polling on app shutdown."""
    polling_task: asyncio.Task = app["polling_task"]
    polling_task.cancel()


async def close_storage(app: Application) -> None:
    """Graceful storage close."""
    storage: BaseStorage = app["storage"]
    await storage.close()
