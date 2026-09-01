from __future__ import annotations

import asyncio
from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from aiohttp import web

from app.telegram.bot import bot_is_available

if TYPE_CHECKING:
    from collections.abc import Coroutine

    from aiohttp.web_app import Application
    from aiohttp.web_request import Request
    from aiohttp.web_response import Response


async def handle_liveness(request: Request) -> Response:
    """Handle liveness request."""
    return await _handle_health(request.app)


async def handle_readiness(request: Request) -> Response:
    """Handle readiness request."""
    return await _handle_health(request.app)


async def _handle_health(app: Application) -> Response:
    """Run health checks and prepare a response."""
    checks: dict[str, Coroutine[Any, Any, bool]] = {}

    if "bot" in app:
        checks["bot"] = bot_is_available(app["bot"])

    results = await _process_checks(checks)
    status, response = _prepare_response(results)
    return web.json_response(response, status=status)


async def _process_checks(
    checks: dict[str, Coroutine[Any, Any, bool]],
) -> dict[str, bool]:
    """Process all checks concurrently and return results."""
    results = await asyncio.gather(*checks.values())
    return dict(zip(checks.keys(), results, strict=True))


def _prepare_response(results: dict[str, bool]) -> tuple[int, dict]:
    """Prepare result response."""
    if all(results.values()):
        return HTTPStatus.OK, {"status": "UP"}
    return HTTPStatus.INTERNAL_SERVER_ERROR, {"status": "DOWN", "detail": results}


def setup(app: Application) -> None:
    """Register handlers."""
    app.router.add_get("/health/liveness", handle_liveness)
    app.router.add_get("/health/readiness", handle_readiness)
