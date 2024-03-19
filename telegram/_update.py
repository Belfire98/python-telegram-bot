#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2024 Leandro Toledo de Souza <devs@python-telegram-bot.org>
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""This module contains an object that represents a Telegram Update."""

from typing import Any, Dict, Final, List, Optional, TypeVar, Union

import telegram
from telegram import constants, TelegramObject
from telegram._callbackquery import CallbackQuery
from telegram._chatboost import ChatBoostRemoved, ChatBoostUpdated
from telegram._chatjoinrequest import ChatJoinRequest
from telegram._chatmemberupdated import ChatMemberUpdated
from telegram._choseninlineresult import ChosenInlineResult
from telegram._inline.inlinequery import InlineQuery
from telegram._message import Message
from telegram._messagereactionupdated import MessageReactionCountUpdated, MessageReactionUpdated
from telegram._payment.precheckoutquery import PreCheckoutQuery
from telegram._payment.shippingquery import ShippingQuery
from telegram._poll import Poll, PollAnswer
from telegram._utils.types import JSONDict
from telegram._utils.warnings import warn


