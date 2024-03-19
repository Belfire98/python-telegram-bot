import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple, Type, Union

import datetime
from telegram import Chat, Message, MessageEntity, Update, User
from tests.auxil.ci_bots import BOT_INFO_PROVIDER
from tests.auxil.pytest_classes import make_bot
from typing_extensions import Final

CMD_PATTERN: Final = re.compile(r"/[\da-z_]{1,32}(?:@\w{1,32})?")
"""Regular expression pattern for matching Telegram commands."""

__version__: Final = "1.0.0"
"""The version of the library."""

__all__: Final = [
    "make_bot",
    "make_command_message",
    "make_command_update",
    "make_message",
    "make_message_update",
]
"""The public API of the library."""


class ChatInfo(NamedTuple):
    """A named tuple for representing a chat."""

    id: int
    type: str


class UserInfo(NamedTuple):
    """A named tuple for representing a user."""

    id: int
    first_name: str
    is_bot: bool


class MessageInfo(NamedTuple):
    """A named tuple for representing a message."""

    message_id: int
    from_user: UserInfo
    date: datetime.datetime
    chat: ChatInfo
    text: str


@dataclass
class MessageEntityInfo:
    """A dataclass for representing a message entity."""

    type: str
    offset: int
    length: int


def make_bot(bot_info: UserInfo = BOT_INFO_PROVIDER.get_info()) -> Type[Update]:
    """
    A factory function for creating a bot instance.

    :param bot_info: The information about the bot.
    :return: A bot instance.
    """
    return make_bot(bot_info)


def make_message(
    text: str,
    *,
    bot: Optional[Type[Update]] = None,
    user: Optional[UserInfo] = None,
    date: Optional[datetime.datetime] = None,
    chat: Optional[ChatInfo] = None,
    entities: Optional[List[MessageEntityInfo]] = None,
    **kwargs: Any,
) -> Message:
    """
    A factory function for creating a message instance.

    :param text: The text of the message.
    :param bot: The bot instance.
    :param user: The user who sent the message.
    :param date: The date and time when the message was sent.
    :param chat: The chat where the message was sent.
    :param entities: The entities in the message.
    :param kwargs: Additional keyword arguments.
    :return: A message instance.
    """
    if bot is None:
        bot = make_bot(BOT_INFO_PROVIDER.get_info())

    message = Message(
        message_id=1,
        from_user=user or UserInfo(id=1, first_name="", is_bot=False),
        date=date or datetime.datetime.utcnow(),
        chat=chat or ChatInfo(id=1, type=""),
        text=text,
        entities=entities or [],
        **kwargs,
    )
    message.set_bot(bot)
    return message


def make_command_message(
    text: str,
    *,
    bot: Optional[Type[Update]] = None,
    user: Optional[UserInfo] = None,
    date: Optional[datetime.datetime] = None,
    chat: Optional[ChatInfo] = None,
    **kwargs: Any,
) -> Message:
    """
    A factory function for creating a message instance that contains a command.

    :param text: The text of the message.
    :param bot: The bot instance.
    :param user: The user who sent the message.
    :param date: The date and time when the message was sent.
    :param chat: The chat where the message was sent.
    :param kwargs: Additional keyword arguments.
    :return: A message instance.
    """
    match = re.search(CMD_PATTERN, text)
    entities = (
        [
            MessageEntity(
                type=MessageEntity.BOT_COMMAND,
                offset=match.start(0),
                length=len(match.group(0)),
            )
        ]
        if match
        else []
    )

    return make_message(text, bot=bot, user=user, date=date, chat=chat, entities=entities, **kwargs)


def make_message_update(
    message: Union[Message, str],
    message_factory: Callable = make_message,
    edited: bool = False,
    **kwargs: Any,
) -> Update:
    """
    A factory function for creating an update instance from a message.

    :param message: The message instance or the text of the message.
    :param message_factory: The factory function for creating a message instance.
    :param edited: Whether the message was edited.
    :param kwargs: Additional keyword arguments.
    :return: An update instance.
   
