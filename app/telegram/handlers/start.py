from typing import cast

from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, User


async def handle_start(message: Message):
    """Handle /start command."""
    user = cast(User, message.from_user)
    await message.answer(f"Hi, {user.full_name}")


def setup(dispatcher: Dispatcher) -> None:
    """Register handlers."""
    dispatcher.message.register(handle_start, Command("start"))
