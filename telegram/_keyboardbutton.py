#!/usr/bin/env python

from typing import Any, ClassVar, Optional

from telegram._keyboardbuttonpolltype import KeyboardButtonPollType
from telegram._keyboardbuttonrequest import (
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUsers,
)
from telegram._telegramobject import TelegramObject
from telegram._utils.types import JSONDict
from telegram._webappinfo import WebAppInfo

if TYPE_CHECKING:
    from telegram import Bot


class KeyboardButton(TelegramObject):
    """
    This object represents one button of the reply keyboard. For simple text buttons, :obj:`str`
    can be used instead of this object to specify text of the button.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`text`, :attr:`request_contact`, :attr:`request_location`,
    :attr:`request_poll`, :attr:`web_app`, :attr:`request_users` and :attr:`request_chat` are
    equal.

    Note:
        * Optional fields are mutually exclusive.
        * :attr:`request_contact` and :attr:`request_location` options will only work in Telegram
          versions released after 9 April, 2016. Older clients will display unsupported message.
        * :attr:`request_poll` option will only work in Telegram versions released after 23
          January, 2020. Older clients will display unsupported message.
        * :attr:`web_app` option will only work in Telegram versions released after 16 April, 2022.
          Older clients will display unsupported message.
        * :attr:`request_users` and :attr:`request_chat` options will only work in Telegram
          versions released after 3 February, 2023. Older clients will display unsupported
          message.

    .. versionchanged:: 21.0
       Removed deprecated argument and attribute ``request_user``.
    .. versionchanged:: 20.0
       :attr:`web_app` is considered as well when comparing objects of this type in terms of
       equality.
    .. versionchanged:: 20.5
       :attr:`request_users` and :attr:`request_chat` are considered as well when
       comparing objects of this type in terms of equality.

    Args:
        text (str): Text of the button. If none of the optional fields are used, it will be
            sent to the bot as a message when the button is pressed.
        request_contact (bool, optional): If True, the user's phone number will be
            sent as a contact when the button is pressed. Available in private chats only.
        request_location (bool, optional): If True, the user's current location will
            be sent when the button is pressed. Available in private chats only.
        request_poll (KeyboardButtonPollType, optional): If specified, the user
            will be asked to create a poll and send it to the bot when the button is pressed.
            Available in private chats only.
        web_app (WebAppInfo, optional): If specified, the described `Web App
            <https://core.telegram.org/bots/webapps>`_ will be launched when the button is pressed.
            The Web App will be able to send a :attr:`Message.web_app_data` service message.
            Available in private chats only.

            .. versionadded:: 20.0

        request_users (KeyboardButtonRequestUsers, optional): If specified, pressing the
            button will open a list of suitable users. Tapping on any user will send its
            identifier to the bot in a :attr:`telegram.Message.users_shared` service message.
            Available in private chats only.

            .. versionadded:: 20.8
        request_chat (KeyboardButtonRequestChat, optional): If specified, pressing the
            button will open a list of suitable chats. Tapping on a chat will send its
            identifier to the bot in a :attr:`telegram.Message.chat_shared` service message.
            Available in private chats only.

            .. versionadded:: 20.1
    Attributes:
        text (str): Text of the button. If none of the optional fields are used, it will be
            sent to the bot as a message when the button is pressed.
        request_contact (bool): Optional. If True, the user's phone number will be
            sent as a contact when the button is pressed. Available in private chats only.
        request_location (bool): Optional. If True, the user's current location will
            be sent when the button is pressed. Available in private chats only.
        request_poll (KeyboardButtonPollType): Optional. If specified,
            the user will be asked to create a poll and send it to the bot when the button is
            pressed. Available in private chats only.
        web_app (WebAppInfo): Optional. If specified, the described `Web App
            <https>`_ will be launched when the button is pressed. The Web App will be able to
            send a :attr:`Message.web_app_data` service message.
            Available in private chats only.

            .. versionadded:: 20.0
        request_users (KeyboardButtonRequestUsers): Optional. If specified, pressing the
            button will open a list of suitable users. Tapping on any user will send its
            identifier to the bot in a :attr:`telegram.Message.users_shared` service message.
            Available in private chats only.

            .. versionadded:: 20.8
        request_chat (KeyboardButtonRequestChat): Optional. If specified, pressing the
            button will open a list of suitable chats. Tapping on a chat will send its
            identifier to the bot in a :attr:`telegram.Message.chat_shared` service
