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
"""This module contains the ChatBoostHandler class."""

from typing import (
    Any,
    Callable,
    Collection,
    Coroutine,
    Final,
    Optional,
    TypeVar,
)

from telegram import (
    Update,
    CallbackContext,
    CHAT_BOOST,
    REMOVED_CHAT_BOOST,
    ANY_CHAT_BOOST,
)
from telegram.ext._handlers.basehandler import BaseHandler
from telegram.ext._utils._update_parsing import parse_chat_id, parse_username
from telegram.ext._utils.types import CCT

CCTT = TypeVar("CCTT", bound=CallbackContext)


class ChatBoostHandler(BaseHandler[Update, CCT]):
    """
    Handler class to handle Telegram updates that contain a chat boost.

    Warning:
        When setting :paramref:`block` to :obj:`False`, you cannot rely on adding custom
        attributes to :class:`telegram.ext.CallbackContext`. See its docs for more info.

    .. versionadded:: 20.8

    Args:
        callback (Callable[[Update, CCTT], Coroutine[Any, Any, None]]): The callback function for this handler. Will be
            called when :meth:`check_update` has determined that an update should be processed by
            this handler. Callback signature::

                async def callback(update: Update, context: CallbackContext)

            The return value of the callback is usually ignored except for the special case of
            :class:`telegram.ext.ConversationHandler`.
        chat_boost_types (int, optional): Pass one of
            :attr:`CHAT_BOOST`, :attr:`REMOVED_CHAT_BOOST` or
            :attr:`ANY_CHAT_BOOST` to specify if this handler should handle only updates with
            :attr:`telegram.Update.chat_boost`,
            :attr:`telegram.Update.removed_chat_boost` or both. Defaults to
            :attr:`CHAT_BOOST`.
        chat_id (int | Collection[int], optional): Filters reactions to allow
            only those which happen in the specified chat ID(s).
        chat_username (str | Collection[str], optional): Filters reactions to allow
            only those which happen in the specified username(s).
        block (bool, optional): Determines whether the return value of the callback should
            be awaited before processing the next handler in
            :meth:`telegram.ext.Application.process_update`. Defaults to :obj:`True`.

            .. seealso:: :wiki:`Concurrency`

    Attributes:
        callback (Callable[[Update, CCTT], Coroutine[Any, Any, None]]): The callback function for this handler.
        chat_boost_types (int): Optional. Specifies if this handler should handle only
            updates with :attr:`telegram.Update.chat_boost`,
            :attr:`telegram.Update.removed_chat_boost` or
