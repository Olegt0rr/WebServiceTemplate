import logging

from aiohttp.web import run_app

from app import app_factory
from app.core.settings import WebAppSettings

logging.basicConfig(level=logging.INFO)

settings = WebAppSettings()
app = app_factory()
run_app(app, host=settings.HOST, port=settings.PORT)
