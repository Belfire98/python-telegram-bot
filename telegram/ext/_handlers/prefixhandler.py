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
"""This module contains the PrefixHandler class."""
import itertools
from typing import TYPE_CHECKING, Any, Dict, FrozenSet, List, Optional, Tuple, TypeVar, Union

from telegram import Update
from telegram._utils.defaultvalue import DEFAULT_TRUE
from telegram._utils.types import SCT, DVType
from telegram.ext import filters as filters_module
from telegram.ext._handlers.basehandler import BaseHandler
from telegram.ext._utils.types import CCT, HandlerCallback

if TYPE_CHECKING:
    from telegram.ext import Application

RT = TypeVar("RT")


class PrefixHandler(BaseHandler[Update, CCT]):
    """Handler class to handle custom prefix commands.

    This is an intermediate handler between :class:`MessageHandler` and :class:`CommandHandler`.
    It supports configurable commands with the same options as :class:`CommandHandler`. It will
    respond to every combination of :paramref:`prefix` and :paramref:`command`.
    It will add a :obj:`list` to the :class:`CallbackContext` named :attr:`CallbackContext.args`,
    containing a list of strings, which is the text following the command split on single or
    consecutive whitespace characters.

    Examples:

        Single prefix and command:

        .. code:: python

            PrefixHandler("!", "test", callback)  # will respond to '!test'.

        Multiple prefixes, single command:

        .. code:: python

            PrefixHandler(["!", "#"], "test", callback)  # will respond to '!test' and '#test'.

        Multiple prefixes and commands:

        .. code:: python

            PrefixHandler(
                ["!", "#"], ["test", "help"], callback
            )  # will respond to '!test', '#test', '!help' and '#help'.


    By default, the handler listens to messages as well as edited messages. To change this behavior
    use :attr:`~filters.UpdateType.EDITED_MESSAGE <telegram.ext.filters.UpdateType.EDITED_MESSAGE>`

    Note:
        * :class:`PrefixHandler` does *not* handle (edited) channel posts.

    Warning:
        When setting :paramref:`block` to :obj:`False`, you cannot rely on adding custom
        attributes to :class:`telegram.ext.CallbackContext`. See its docs for more info.

    .. versionchanged:: 20.0

        * :class:`PrefixHandler` is no longer a subclass of :class:`CommandHandler`.
        * Removed the attributes ``command`` and ``prefix``. Instead, the new :attr:`commands`
          contains all commands that this handler listens to as a :class:`frozenset`, which
          includes the prefixes.
        * Updating the prefixes and commands this handler listens to is no longer possible.

    Args:
        prefix (Union[str, Sequence[str]]):
            The prefix(es) that will precede :paramref:`command`.
        command (Union[str, Sequence[str]]):
            The command or list of commands this handler should listen for. Case-insensitive.
        callback (HandlerCallback[Update, CCT, RT]): The callback function for this handler. Will be
            called when :meth:`check_update` has determined that an update should be processed by
            this handler. Callback signature::

                async def callback(update: Update, context: CallbackContext)

            The return value of the callback is usually ignored except for the special case of
            :class:`telegram.ext.ConversationHandler`.
        filters (Optional[filters_module.BaseFilter] = None): A filter inheriting from
            :class:`telegram.ext.filters.BaseFilter`. Standard filters can be found in
            :mod:`telegram.ext.filters`. Filters can be combined using bitwise
            operators (``&`` for :keyword:`and`, ``|`` for :keyword:`or`, ``
