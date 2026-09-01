import logging

from aiohttp.web import run_app

from app import app_factory
from app.core.settings import WebAppSettings

try:
    import uvloop
except ImportError:
    uvloop = None  # type: ignore[assignment]

logging.basicConfig(level=logging.INFO)

settings = WebAppSettings()
app = app_factory()
loop = uvloop.new_event_loop() if uvloop else None
run_app(app, host=settings.HOST, port=settings.PORT, loop=loop)
