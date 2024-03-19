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
"""This module contains the TypeHandler class."""

from typing import Optional, Type, TypeVar, overload

from telegram._utils.defaultvalue import DEFAULT_TRUE
from telegram._utils.types import CCT, HandlerCallback
from telegram.ext._handlers.basehandler import BaseHandler
from telegram.ext._utils.types import DVType

RT = TypeVar("RT")
UT = TypeVar("UT")

class TypeHandler(BaseHandler[UT, CCT]):
    """Handler class to handle updates of custom types.

    Warning:
        When setting :paramref:`block` to :obj:`False`, you cannot rely on adding custom
        attributes to :class:`telegram.ext.CallbackContext`. See its docs for more info.

    Args:
        update_type (type[UT]): The type of updates this handler should process, as determined by :obj:`isinstance`
        callback (HandlerCallback[UT, CCT, RT]): The callback function for this handler. Will be
            called when :meth:`check_update` has determined that an update should be processed by
            this handler. Callback signature::

                async def callback(update: Update, context: CallbackContext)

            The return value of the callback is usually ignored except for the special case of
            :class:`telegram.ext.ConversationHandler`.
        strict (bool = False): Use `update_type` instead of :obj:`isinstance`.
            Default is :obj:`False`.
        block (DVType[bool] = DEFAULT_TRUE): Determines whether the return value of the callback should
            be awaited before processing the next handler in
            :meth:`telegram.ext.Application.process_update`. Defaults to :obj:`True`.

            .. seealso:: :wiki:`Concurrency`

    Attributes:
        update_type (type[UT]): The type of updates this handler should process.
        callback (HandlerCallback[UT, CCT, RT]): The callback function for this handler.
        strict (bool): Use `update_type` instead of :obj:`isinstance`. Default is
            :obj:`False`.
        block (bool): Determines whether the return value of the callback should be
            awaited before processing the next handler in
            :meth:`telegram.ext.Application.process_update`.

    """

    __slots__ = ("strict", "update_type")

    def __init__(
        self,
        update_type: Type[UT],
        callback: HandlerCallback[UT, CCT, RT],
        strict: bool = False,
        block: DVType[bool] = DEFAULT_TRUE,
    ):
        super().__init__(callback, block=block)
        self.update_type: Type[UT] = update_type
        self.strict: Optional[bool] = strict

    @overload
    def check_update(self, update: UT) -> bool: ...

    @overload
    def check_update(self, update: object) -> bool: ...

    def check_update(self, update: object) -> bool:
        """Determines whether an update should be passed to this handler's :attr:`callback`.

        Args:
            update (object): Incoming update.

        Returns:
            bool

        """
        if not self.strict:
            return isinstance(update, self.update_type)
        return type(update) is self.update_type  # pylint: disable=unidiomatic-typecheck
