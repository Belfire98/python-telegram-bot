#!/usr/bin/env python

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from telegram._chatadministratorights import ChatAdministratorRights
from telegram._telegramobject import TelegramObject
from telegram._utils.types import JSONDict

if TYPE_CHECKING:
    from telegram import Bot


class KeyboardButtonRequestUsers(TelegramObject):
    """
    This object defines the criteria used to request a suitable user.
    The identifier of the selected user will be shared with the bot when the
    corresponding button is pressed.

    Args:
        request_id (int): Signed 32-bit identifier of the request, which will be received
            back in the :class:`telegram.UsersShared` object. Must be unique within the message.
        user_is_bot (bool, optional): Pass :obj:`True` to request a bot, pass :obj:`False`
            to request a regular user. If not specified, no additional restrictions are applied.
        user_is_premium (bool, optional): Pass :obj:`True` to request a premium user, pass
            :obj:`False` to request a non-premium user. If not specified, no additional
            restrictions are applied.
        max_quantity (int, optional): The maximum number of users to be selected;
            :tg-const:`telegram.constants.KeyboardButtonRequestUsersLimit.MIN_QUANTITY` -
            :tg-const:`telegram.constants.KeyboardButtonRequestUsersLimit.MAX_QUANTITY`.
            Defaults to :tg-const:`telegram.constants.KeyboardButtonRequestUsersLimit.MIN_QUANTITY`
            .

            .. versionadded:: 20.8

    Attributes:
        request_id (int): Identifier of the request.
        user_is_bot (bool): Optional. Pass :obj:`True` to request a bot, pass :obj:`False`
            to request a regular user. If not specified, no additional restrictions are applied.
        user_is_premium (bool): Optional. Pass :obj:`True` to request a premium user, pass
            :obj:`False` to request a non-premium user. If not specified, no additional
            restrictions are applied.
        max_quantity (int): Optional. The maximum number of users to be selected;
            :tg-const:`telegram.constants.KeyboardButtonRequestUsersLimit.MIN_QUANTITY` -
            :tg-const:`telegram.constants.KeyboardButtonRequestUsersLimit.MAX_QUANTITY`.
            Defaults to :tg-const:`telegram.constants.KeyboardButtonRequestUsersLimit.MIN_QUANTITY`
            .

            .. versionadded:: 20.8
    """

    __slots__ = (
        "max_quantity",
        "request_id",
        "user_is_bot",
        "user_is_premium",
    )

    def __init__(
        self,
        request_id: int,
        user_is_bot: Optional[bool] = None,
        user_is_premium: Optional[bool] = None,
        max_quantity: Optional[int] = None,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(api_kwargs=api_kwargs)
        # Required
        self.request_id: int = request_id

        # Optionals
        self.user_is_bot: Optional[bool] = user_is_bot
        self.user_is_premium: Optional[bool] = user_is_premium
        self.max_quantity: Optional[int] = max_quantity

        self._id_attrs = (self.request_id,)

        self._freeze()

