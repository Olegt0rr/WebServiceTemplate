from aiogram import Dispatcher

from . import start


def setup(dispatcher: Dispatcher) -> None:
    """Setup handlers."""
    start.setup(dispatcher)
