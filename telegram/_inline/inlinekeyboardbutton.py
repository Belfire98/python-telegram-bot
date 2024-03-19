#!/usr/bin/env python

import typing as ty
from telegram import constants, TelegramObject, LoginUrl, WebAppInfo, CallbackGame, SwitchInlineQueryChosenChat

if ty.TYPE_CHECKING:
    from telegram import Bot

class InlineKeyboardButton(TelegramObject):
    """
    This object represents one button of an inline keyboard.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`text`, :attr:`url`, :attr:`login_url`, :attr:`callback_data`,
    :attr:`switch_inline_query`, :attr:`switch_inline_query_current_chat`, :attr:`callback_game`,
    :attr:`web_app` and :attr:`pay` are equal.

    Note:
        * You must use exactly one of the optional fields. Mind that :attr:`callback_game` is not
          working as expected. Putting a game short name in it might, but is not guaranteed to
          work.
        * If your bot allows for arbitrary callback data, in keyboards returned in a response
          from telegram, :attr:`callback_data` maybe be an instance of
          :class:`telegram.ext.InvalidCallbackData`. This will be the case, if the data
          associated with the button was already deleted.

          .. versionadded:: 13.6

        * Since Bot API 5.5, it's now allowed to mention users by their ID in inline keyboards.
          This will only work in Telegram versions released after December 7, 2
