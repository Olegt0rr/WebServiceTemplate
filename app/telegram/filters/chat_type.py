from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.filters import BaseFilter

if TYPE_CHECKING:
    from aiogram.types import Chat, TelegramObject


class ChatType(BaseFilter):
    """Represents chat type filter."""

    def __init__(self, chat_type: str | set[str]) -> None:
        self._check_type(chat_type)
        self.chat_type = chat_type

    async def __call__(self, object_: TelegramObject) -> bool:
        """Apply filter."""
        chat = self._get_chat(object_)
        if isinstance(self.chat_type, str):
            return chat.type == self.chat_type
        return chat.type in self.chat_type

    @staticmethod
    def _get_chat(object_: TelegramObject) -> Chat:
        """Get chat from Telegram object."""
        if hasattr(object_, "chat"):
            return object_.chat

        if hasattr(object_, "message"):
            return object_.message.chat

        msg = f"Can't find Chat in {type(object_).__name__} object."
        raise RuntimeError(msg)

    @staticmethod
    def _check_type(chat_type: str | set[str]) -> None:
        """Raise error if chat_type is not supported."""
        if not isinstance(chat_type, (str, set)):
            msg = (
                f"Unsupported chat type: {type(chat_type).__name__}. "
                f"Use `str` or `set` instead."
            )
            raise TypeError(msg)
