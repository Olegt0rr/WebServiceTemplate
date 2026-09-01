from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING

import pytest
from aiogram import Bot
from aiogram.types import User

# Force test-safe settings: never talk to a real bot, never start polling.
# Plain assignment (not setdefault) so a real token exported in the developer's
# shell can't leak into the test run.
os.environ["TELEGRAM_TOKEN"] = "42:TEST"
os.environ["TELEGRAM_WEBHOOK_ENABLED"] = "true"

from app import app_factory

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from aiohttp.web_app import Application
    from pytest_aiohttp.plugin import AiohttpClient


@pytest.fixture(autouse=True)
def _mock_bot_api(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep tests offline: replace the Telegram API call behind health checks."""

    async def get_me(self: Bot) -> User:
        return User(id=42, is_bot=True, first_name="Test", username="test_bot")

    monkeypatch.setattr(Bot, "get_me", get_me)


@pytest.fixture(name="app")
def app_fixture() -> Application:
    """Prepare default web app."""
    return app_factory()


@pytest.fixture(name="http_client")
async def http_client_fixture(
    app: Application,
    aiohttp_client: AiohttpClient,
) -> ClientSession:
    """Prepare client session for app."""
    client = await aiohttp_client(app)

    yield client

    await client.close()

    # Wait 250 ms for the underlying SSL connections to close
    # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
    await asyncio.sleep(0.25)
