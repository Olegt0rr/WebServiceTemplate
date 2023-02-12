import logging

from aiogram import Dispatcher

from . import handlers
from .storage import create_storage

logger = logging.getLogger(__name__)


def create_dispatcher() -> Dispatcher:
    """Create dispatcher for Telegram."""
    storage = create_storage()
    dispatcher = Dispatcher(storage=storage)
    handlers.setup(dispatcher)

    logger.debug("Dispatcher %r created.", dispatcher)
    return dispatcher
