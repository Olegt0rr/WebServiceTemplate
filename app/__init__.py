from aiohttp.web_app import Application

from .core.setup import setup_core
from .redis.setup import setup_redis
from .telegram.setup import setup_telegram


def app_factory() -> Application:
    """Create web app.

    Warning! Setup order matters!
    """
    app = Application()

    setup_redis(app)
    setup_telegram(app)
    setup_core(app)

    return app
