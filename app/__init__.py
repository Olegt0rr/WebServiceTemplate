from aiohttp.web_app import Application

from .core.handlers import setup_routes
from .telegram.setup import setup_telegram


def app_factory() -> Application:
    """Create web app."""
    app = Application()

    setup_routes(app)
    setup_telegram(app)

    return app
