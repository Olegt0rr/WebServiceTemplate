from __future__ import annotations

from typing import TYPE_CHECKING

from .handlers import setup_handlers

if TYPE_CHECKING:
    from aiohttp.web_app import Application


def setup_core(app: Application) -> None:
    """Set up core service."""
    setup_handlers(app)
