#!/usr/bin/env python

"""This module contains objects representing Telegram bot command scopes."""

from typing import Dict, Final, Optional, Type, Union

from telegram import constants
from telegram._telegramobject import TelegramObject
from telegram._utils import enum
from telegram._utils.types import JSONDict

if TYPE_CHECKING:
    from telegram import Bot


class BotCommandScope(TelegramObject):
    """Base class for objects that represent the scope to which bot commands are applied.
    Currently, the following 7 scopes are supported:

    * :class:`telegram.BotCommandScopeDefault`
    * :class:`telegram.BotCommandScopeAllPrivateChats`
    * :class:`telegram.BotCommandScopeAllGroupChats`
    * :class:`telegram.BotCommandScopeAllChatAdministrators`
    * :class:`telegram.BotCommandScopeChat`
    * :class:`telegram.BotCommandScopeChatAdministrators`
    * :class:`telegram.BotCommandScopeChatMember`

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`scope_type` is equal. For subclasses with additional
    attributes, the notion of equality is overridden.

    Note:
        Please see the `official docs`_ on how Telegram determines which commands to display.

    .. _`official docs`: https://core.telegram.org/bots/api#determining-list-of-commands

    .. versionadded:: 13.7

    Args:
        scope_type (str): Scope type.

    Attributes:
        scope_type (str): Scope type.
    """

    __slots__ = ("scope_type",)

    DEFAULT: Final[str] = constants.BotCommandScopeType.DEFAULT
    """:const:`telegram.constants.BotCommandScopeType.DEFAULT`"""
    ALL_PRIVATE_CHATS: Final[str] = constants.BotCommandScopeType.ALL_PRIVATE_CHATS
    """:const:`telegram.constants.BotCommandScopeType.ALL_PRIVATE_CHATS`"""
    ALL_GROUP_CHATS: Final[str] = constants.BotCommandScopeType.ALL_GROUP_CHATS
    """:const:`telegram.constants.BotCommandScopeType.ALL_GROUP_CHATS`"""
    ALL_CHAT_ADMINISTRATORS: Final[str] = constants.BotCommandScopeType.ALL_CHAT_ADMINISTRATORS
    """:const:`telegram.constants.BotCommandScopeType.ALL_CHAT_ADMINISTRATORS`"""
    CHAT: Final[str] = constants.BotCommandScopeType.CHAT
    """:const:`telegram.constants.BotCommandScopeType.CHAT`"""
    CHAT_ADMINISTRATORS: Final[str] = constants.BotCommandScopeType.CHAT_ADMINISTRATORS
    """:const:`telegram.constants.BotCommandScopeType.CHAT_ADMINISTRATORS`"""
    CHAT_MEMBER: Final[str] = constants.BotCommandScopeType.CHAT_MEMBER
    """:const:`telegram.constants.BotCommandScopeType.CHAT_MEMBER`"""

    def __init__(self, scope_type: str, *, api_kwargs: Optional[JSONDict] = None):
        super().__init__(api_kwargs=api_kwargs)
        self.scope_type: str = enum.get_member(constants.BotCommandScopeType, scope_type, scope_type)
        self._id_attrs = (self.scope_type,)

        self._freeze()

    @classmethod
    def from_dict(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["BotCommandScope"]:
        """Converts dictionary data to the appropriate :class:`BotCommandScope` object, i.e. takes
        care of selecting the correct subclass.

        Args:
            data (Dict[:obj:`str`, ...]): The dictionary data.
            bot (:class:`telegram.Bot`): The bot associated with this object.

        Returns:
            The Telegram object.

        """
        data = cls._parse_data(data)

        if not data:
            return None

        _class_mapping: Dict[str, Type[BotCommandScope]] = {
            cls.DEFAULT: BotCommandScopeDefault,
            cls.ALL_PRIVATE_CHATS: BotCommandScopeAllPrivateChats,
            cls.ALL_GROUP_CHATS: BotCommandScopeAllGroupChats,
            cls.ALL_CHAT_ADMINISTRATORS: BotCommandScopeAllChatAdministrators,
            cls.CHAT: BotCommandScopeChat,
            cls.CHAT_ADMINISTRATORS: BotCommandScopeChatAdministrators,
            cls.CHAT_MEMBER: BotCommandScopeChatMember,
        }

        if cls is BotCommandScope and scope_type in _class_mapping:
            return _class_mapping[scope_type].from_dict(data=data, bot=bot)
        return super().from_dict(data=data, bot=bot)

    @property
    def scope_type(self) -> str:
        """The scope type."""
        return self.type

    @scope_type.setter
    def scope_type(self, value: str):
        self.type = value

    def __repr__(self):
        return f"<{self.__class__.__name__} scope_type={self.scope_type}>"


class BotCommandScopeDefault(BotCommandScope):
    """Represents the default scope of bot commands. Default commands are used if no commands
    with a `narrower scope`_ are specified for the user.

    .. _`
