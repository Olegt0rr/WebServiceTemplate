from __future__ import annotations

import asyncio
import logging
import ssl
from typing import TYPE_CHECKING, Any

import backoff
from aiohttp import ClientError, ClientSession, TCPConnector
from msgspec.json import Decoder, Encoder

if TYPE_CHECKING:
    from collections.abc import Mapping

    from yarl import URL


class BaseClient:
    """Represents base API client."""

    def __init__(self, base_url: str | URL) -> None:
        self._base_url = base_url
        self._session: ClientSession | None = None
        self.log = logging.getLogger(self.__class__.__name__)
        self._decoder = Decoder()

    async def _get_session(self) -> ClientSession:
        """Get aiohttp session with cache."""
        if self._session is None or self._session.closed:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.load_default_certs()
            connector = TCPConnector(ssl_context=ssl_context)
            encoder = Encoder()
            self._session = ClientSession(
                base_url=self._base_url,
                connector=connector,
                json_serialize=lambda obj: str(encoder.encode(obj), "utf-8"),
            )

        return self._session

    @backoff.on_exception(backoff.expo, ClientError, max_time=60)
    async def _make_request(
        self,
        method: str,
        url: str | URL,
        params: Mapping[str, str] | None = None,
        json: Mapping[str, str] | None = None,
    ) -> tuple[int, dict[str, Any]]:
        """Make request and return decoded json response."""
        session = await self._get_session()

        self.log.debug(
            "Making request %r %r with json %r and params %r",
            method,
            url,
            json,
            params,
        )
        async with session.request(method, url, params=params, json=json) as response:
            status = response.status
            result = await response.json(loads=self._decoder.decode)

        self.log.debug(
            "Got response %r %r with status %r and json %r",
            method,
            url,
            status,
            result,
        )
        return status, result

    async def close(self) -> None:
        """Graceful session close."""
        if not self._session:
            self.log.debug("There's not session to close.")
            return

        if self._session.closed:
            self.log.debug("Session already closed.")
            return

        await self._session.close()
        self.log.debug("Session successfully closed.")

        # Wait 250 ms for the underlying SSL connections to close
        # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        await asyncio.sleep(0.25)
