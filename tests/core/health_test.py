from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiohttp import ClientSession


async def test_liveness(http_client: ClientSession) -> None:
    """Test liveness answers OK."""
    async with http_client.get("/health/liveness") as response:
        assert response.status == HTTPStatus.OK


async def test_readiness(http_client: ClientSession) -> None:
    """Test readiness answers OK."""
    async with http_client.get("/health/readiness") as response:
        assert response.status == HTTPStatus.OK
