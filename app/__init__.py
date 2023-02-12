from aiohttp.web_app import Application

from app.telegram.setup import setup_telegram


def app_factory() -> Application:
    """Create web app."""
    app = Application()
    setup_telegram(app)
    return app
