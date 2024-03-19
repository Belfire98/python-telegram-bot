#!/usr/bin/env python

"""
A library that provides a Python interface to the Telegram Bot API
Copyright (C) 2015-2024 
Leandro Toledo de Souza <devs@python-telegram-bot.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser Public License for more details.

You should have received a copy of the GNU Lesser Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import TYPE_CHECKING, Optional

import json
from telegram._chat import Chat
from telegram._telegramobject import TelegramObject
from telegram._utils.types import JSONDict

if TYPE_CHECKING:
    from telegram import Bot


class Story(TelegramObject):
    """
    This object represents a story.

    Args:
        chat (Chat): Chat that posted the story.
        story_id (int): Unique identifier for the story in the chat.

    Attributes:
        chat (Chat): Chat that posted the story.
        story_id (int): Unique identifier for the story in the chat.

    """

    __slots__ = (
        "chat",
        "story_id",
    )

    def __init__(
        self,
        chat: Chat,
        story_id: int,  # pylint: disable=redefined-builtin
        *,
        api_kwargs: Optional[JSONDict] = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        self.chat: Chat = chat
        self.story_id: int = story_id

        self._id_attrs = (self.chat, self.story_id)

        self._freeze()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Story):
            return self.chat == other.chat and self.story_id == other.story_id
        return False

    def __hash__(self) -> int:
        return hash((self.chat, self.story_id))

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["Story"]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if not data:
            return None

        data["chat"] = Chat.de_json(data.get("chat", {}), bot)
        return super().de_json(data=data, bot=bot)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} chat={self.chat} story_id={self.story_id}>"
        )
