from typing import TYPE_CHECKING

from . import health

if TYPE_CHECKING:
    from aiohttp.web_app import Application


def setup_routes(app: "Application") -> None:
    """Register handlers."""
    health.setup(app)
