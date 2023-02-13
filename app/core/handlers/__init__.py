from typing import TYPE_CHECKING

from . import k8s

if TYPE_CHECKING:
    from aiohttp.web_app import Application


def setup_routes(app: "Application") -> None:
    """Register handlers."""
    k8s.setup(app)
