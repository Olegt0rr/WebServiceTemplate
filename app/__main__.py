import logging
from contextlib import suppress

from aiohttp.web import run_app

from app import app_factory
from app.core.settings import WebAppSettings

with suppress(ImportError):
    import uvloop

    uvloop.install()

logging.basicConfig(level=logging.INFO)

settings = WebAppSettings()
app = app_factory()
run_app(app, host=settings.HOST, port=settings.PORT)
