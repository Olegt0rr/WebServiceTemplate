from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from app.core.handlers import health

if TYPE_CHECKING:
    from aiogram import Bot
    from aiohttp import ClientSession
    from pytest import MonkeyPatch  # noqa: PT013


async def test_liveness(http_client: ClientSession) -> None:
    """Test liveness answers OK."""
    async with http_client.get("/health/liveness") as response:
        assert response.status == HTTPStatus.OK


async def test_readiness(http_client: ClientSession) -> None:
    """Test readiness answers OK."""
    async with http_client.get("/health/readiness") as response:
        assert response.status == HTTPStatus.OK


async def test_liveness_down(
    http_client: ClientSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test liveness answers 500 when a check fails."""

    async def check_failed(bot: Bot) -> bool:
        return False

    monkeypatch.setattr(health, "bot_is_available", check_failed)

    async with http_client.get("/health/liveness") as response:
        assert response.status == HTTPStatus.INTERNAL_SERVER_ERROR
        payload = await response.json()
        assert payload["status"] == "DOWN"
        assert payload["detail"] == {"bot": False}


async def test_liveness_check_raises(
    http_client: ClientSession,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test a raising check fails closed with a structured DOWN response."""

    async def check_broken(bot: Bot) -> bool:
        msg = "boom"
        raise RuntimeError(msg)

    monkeypatch.setattr(health, "bot_is_available", check_broken)

    async with http_client.get("/health/liveness") as response:
        assert response.status == HTTPStatus.INTERNAL_SERVER_ERROR
        payload = await response.json()
        assert payload["status"] == "DOWN"
        assert payload["detail"] == {"bot": False}
