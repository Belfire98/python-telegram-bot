#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2024
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
"""This module contains a class that represents a Telegram SwitchInlineQueryChosenChat."""
from typing import Any, Dict, Optional

from telegram._telegramobject import TelegramObject
from telegram._utils.types import JSONDict


class SwitchInlineQueryChosenChat(TelegramObject):
    """
    This object represents an inline button that switches the current user to inline mode in a
    chosen chat, with an optional default inline query.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`query`, :attr:`allow_user_chats`, :attr:`allow_bot_chats`,
    :attr:`allow_group_chats`, and :attr:`allow_channel_chats` are equal.

    .. versionadded:: 20.3

    Caution:
        The PTB team has discovered that you must pass at least one of
        :paramref:`allow_user_chats`, :paramref:`allow_bot_chats`, :paramref:`allow_group_chats`,
        or :paramref:`allow_channel_chats` to Telegram. Otherwise, an error will be raised.

    Args:
        query (:obj:`str`, optional): The default inline query to be inserted in the input field.
            If left empty, only the bot's username will be inserted.
        allow_user_chats (:obj:`bool`, optional): Pass :obj:`True`, if private chats with users
            can be chosen.
        allow_bot_chats (:obj:`bool`, optional): Pass :obj:`True`, if private chats with bots can
            be chosen.
        allow_group_chats (:obj:`bool`, optional): Pass :obj:`True`, if group and supergroup chats
            can be chosen.
        allow_channel_chats (:obj:`bool`, optional): Pass :obj:`True`, if channel chats can be
            chosen.
        api_kwargs (:obj:`dict`, optional): Additional keyword arguments for the constructor of
            :class:`telegram._telegramobject.TelegramObject`.

    Attributes:
        query (:obj:`str`, optional): The default inline query to be inserted in the input field.
            If left empty, only the bot's username will be inserted.
        allow_user_chats (:obj:`bool`, optional): :obj:`True`, if private chats with users can be
            chosen.
        allow_bot_chats (:obj:`bool`, optional): :obj:`True`, if private chats with bots can be
            chosen.
        allow_group_chats (:obj:`bool`, optional): :obj:`True`, if group and supergroup chats can
            be chosen.
        allow_channel_chats (:obj:`bool`, optional): :obj:`True`, if channel chats can be chosen.

    """

    __slots__ = (
        "allow_bot_chats",
        "allow_channel_chats",
        "allow_group_chats",
        "allow_user_chats",
        "query",
    )

    def __init__(
        self,
        query: Optional[str] = None,
        allow_user_chats: Optional[bool] = None,
        allow_bot_chats: Optional[bool] = None,
        allow_group_chats: Optional[bool] = None,
        allow_channel_chats: Optional[bool] = None,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(api_kwargs=api_kwargs)
        self.__post_init__()

    def __post_init__(self):
        # Set default values for optional attributes
        if self.allow_user_chats is None:
            self.allow_user_chats = False
        if self.allow_bot_chats is None:
            self.allow_bot_chats = False
        if self.allow_group_chats is None:
            self.allow_group_chats = False
        if self.allow_channel_chats is None:
            self.allow_channel_chats = False

        # Check that at least one of the allow_*_chats attributes is set to True
        if not (
            self.allow_user_chats
            or self.allow_bot_chats
            or self.allow_group_chats
            or self.allow_channel_chats
        ):
            raise ValueError(
                "At least one of allow_user_chats, allow_bot_chats, allow_group_chats, or "
                "allow_channel_chats must be set to True."
            )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SwitchInlineQueryChosenChat":
        """
        Create an instance of SwitchInline
