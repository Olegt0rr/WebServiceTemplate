from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aiogram import Dispatcher

from . import handlers

if TYPE_CHECKING:
    from aiogram.fsm.storage.base import BaseStorage

logger = logging.getLogger(__name__)


def create_dispatcher(storage: BaseStorage) -> Dispatcher:
    """Create dispatcher for Telegram."""
    dispatcher = Dispatcher(storage=storage)
    handlers.setup(dispatcher)

    logger.debug("Dispatcher %r created.", dispatcher)
    return dispatcher
