from typing import TYPE_CHECKING, Any

from aiohttp import web

from app.telegram.bot import bot_is_available

if TYPE_CHECKING:
    from collections.abc import Coroutine

    from aiohttp.web_app import Application
    from aiohttp.web_request import Request
    from aiohttp.web_response import Response


async def handle_liveness(request: "Request") -> "Response":
    """Handle liveness request."""
    checks: dict[str, Coroutine[Any, Any, bool]] = {
        "telegram": bot_is_available(request.app["bot"]),
    }
    results = await _process_checks(checks)
    response = _prepare_response(results)
    return web.json_response(response)


async def handle_readiness(request: "Request") -> "Response":
    """Handle readiness request."""
    checks: dict[str, Coroutine[Any, Any, bool]] = {
        "telegram": bot_is_available(request.app["bot"]),
    }
    results = await _process_checks(checks)
    response = _prepare_response(results)
    return web.json_response(response)


async def _process_checks(
    checks: "dict[str, Coroutine[Any, Any, bool]]",
) -> dict[str, bool]:
    """Process all checks and return results."""
    return {name: await check for name, check in checks.items()}


def _prepare_response(results: dict[str, bool]) -> dict:
    """Prepare result response."""
    if all(results.items()):
        return {"status": "UP"}
    return {"status": "DOWN", "detail": results}


def setup(app: "Application") -> None:
    """Register handlers."""
    app.router.add_get("/health/liveness", handle_liveness)
    app.router.add_get("/health/readiness", handle_readiness)
