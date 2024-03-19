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
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains two objects used for request chats/users service messages."""
from typing import Dict, Optional, Sequence, Tuple, Union

from telegram._telegramobject import TelegramObject
from telegram._utils.types import JSONDict


class UsersShared(TelegramObject):
    """
    This object contains information about the user whose identifier was shared with the bot
    using a :class:`telegram.KeyboardButtonRequestUsers` button.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`request_id` and :attr:`user_ids` are equal.

    .. versionadded:: 20.8
       Bot API 7.0 replaces ``UserShared`` with this class. The only difference is that now
       the :attr:`user_ids` is a sequence instead of a single integer.

    Args:
        request_id (:obj:`int`): Identifier of the request.
        user_ids (Sequence[:obj:`int`]): Identifiers of the shared users. These numbers may have
            more than 32 significant bits and some programming languages may have difficulty/silent
            defects in interpreting them. But they have at most 52 significant bits, so 64-bit
            integers or double-precision float types are safe for storing these identifiers. The
            bot may not have access to the users and could be unable to use these identifiers,
            unless the users are already known to the bot by some other means.

    Attributes:
        request_id (:obj:`int`): Identifier of the request.
        user_ids (Tuple[:obj:`int`]): Identifiers of the shared users. These numbers may have
            more than 32 significant bits and some programming languages may have difficulty/silent
            defects in interpreting them. But they have at most 
