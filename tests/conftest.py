import asyncio
from typing import TYPE_CHECKING

import pytest
from app import app_factory

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from aiohttp.web_app import Application
    from pytest_aiohttp.plugin import AiohttpClient


@pytest.fixture(name="app", scope="session")
def app_fixture() -> "Application":
    """Prepare default web app."""
    return app_factory()


@pytest.fixture(name="http_client")
async def http_client_fixture(
    app: "Application",
    aiohttp_client: "AiohttpClient",
) -> "ClientSession":
    """Prepare client session for app."""
    client = await aiohttp_client(app)

    yield client

    await client.close()
    await asyncio.sleep(0.2)
