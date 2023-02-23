from __future__ import annotations

from typing import TYPE_CHECKING, cast

from aiogram.filters import Command
from aiogram.types import User

if TYPE_CHECKING:
    from aiogram import Dispatcher
    from aiogram.types import Message


async def handle_start(message: Message) -> None:
    """Handle /start command."""
    user = cast(User, message.from_user)
    await message.answer(f"Hi, {user.full_name}")


def setup(dispatcher: Dispatcher) -> None:
    """Register handlers."""
    dispatcher.message.register(handle_start, Command("start"))
