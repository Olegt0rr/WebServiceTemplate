from __future__ import annotations

import asyncio
from contextlib import suppress
from typing import TYPE_CHECKING

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

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
        # Wire dispatcher startup/shutdown events (and bot session close).
        setup_application(app, dispatcher, bot=bot)
    else:
        app.on_startup.append(start_polling)
        app.on_shutdown.append(stop_polling)
        app.on_shutdown.append(close_bot)

    app.on_shutdown.append(close_storage)


async def start_polling(app: Application) -> None:
    """Start Telegram polling on app startup."""
    dispatcher: Dispatcher = app["dispatcher"]
    bot: Bot = app["bot"]
    # aiohttp owns the process lifecycle; aiogram must not install
    # its own SIGINT/SIGTERM handlers over aiohttp's.
    polling_coroutine = dispatcher.start_polling(bot, handle_signals=False)
    app["polling_task"] = asyncio.create_task(polling_coroutine)


async def stop_polling(app: Application) -> None:
    """Stop Telegram polling on app shutdown."""
    polling_task: asyncio.Task = app["polling_task"]
    polling_task.cancel()
    with suppress(asyncio.CancelledError):
        await polling_task


async def close_bot(app: Application) -> None:
    """Graceful bot session close."""
    bot: Bot = app["bot"]
    await bot.session.close()


async def close_storage(app: Application) -> None:
    """Graceful storage close."""
    storage: BaseStorage = app["storage"]
    await storage.close()
