import asyncio
import ssl
from typing import TYPE_CHECKING, Any, Optional, Union

import backoff
from aiohttp import ClientError, ClientSession, TCPConnector
from ujson import dumps, loads

if TYPE_CHECKING:
    from collections.abc import Mapping

    from yarl import URL


class BaseClient:
    """Represents base API client."""

    def __init__(self, base_url: "Union[str, URL]") -> None:
        self._base_url = base_url
        self._session: ClientSession | None = None

    async def _get_session(self) -> ClientSession:
        """Get aiohttp session with cache."""
        if not self._session:
            self._session = ClientSession(
                base_url=self._base_url,
                connector=TCPConnector(ssl_context=ssl.SSLContext()),
                json_serialize=dumps,
            )
        return self._session

    @backoff.on_exception(backoff.expo, ClientError, max_time=60)
    async def _make_request(
        self,
        method: str,
        url: "Union[str, URL]",
        params: "Optional[Mapping[str, str]]" = None,
        json: "Mapping[str, str] | None" = None,
    ) -> dict[str, Any]:
        """Make request and return decoded json response."""
        session = await self._get_session()
        async with session.request(method, url, params=params, json=json) as response:
            return await response.json(loads=loads)

    async def close(self) -> None:
        """Graceful session close."""
        if not self._session:
            return

        if self._session.closed:
            return

        await self._session.close()
        await asyncio.sleep(0.2)
