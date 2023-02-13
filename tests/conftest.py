import ssl

import pytest
import ujson
from aiohttp import ClientSession, TCPConnector


@pytest.fixture(scope="session", name="http_client")
async def http_client_fixture() -> ClientSession:
    """Create aiohttp session."""
    session = ClientSession(
        connector=TCPConnector(ssl_context=ssl.SSLContext()),
        json_serialize=ujson.dumps,
    )
    yield session
    await session.close()
