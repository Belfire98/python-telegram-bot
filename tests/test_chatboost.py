# python-telegram-bot - a Python interface to the Telegram Bot API
# Copyright (C) 2015-2024
# by the python-telegram-bot contributors <devs@python-telegram-bot.org>
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

import datetime
import inspect
import unittest.mock
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional

import pytest
from telegram import (
    Chat,
    ChatBoost,
    ChatBoostAdded,
    ChatBoostRemoved,
    ChatBoostSource,
    ChatBoostSourceGiftCode,
    ChatBoostSourceGiveaway,
    ChatBoostSourcePremium,
    ChatBoostUpdated,
    Dice,
    User,
    UserChatBoosts,
)
from telegram._utils.datetime import to_timestamp, UTC
from telegram.constants import ChatBoostSources
from telegram.request import RequestData
from tests.auxil.slots import mro_slots


class ChatBoostDefaults:
    chat_id: int = 1
    boost_id: str = "2"
    giveaway_message_id: int = 3
    is_unclaimed: bool = False
    chat: Chat = Chat(1, "group")
    user: User = User(1, "user", False)
    date: datetime.datetime = to_timestamp(datetime.datetime.utcnow())
    default_source: ChatBoostSourcePremium = ChatBoostSourcePremium(user=User(1, "user", False))


@pytest.fixture(scope="module")
def chat_boost_removed():
    return ChatBoostRemoved(
        chat=ChatBoostDefaults.chat,
        boost_id=ChatBoostDefaults.boost_id,
        remove_date=ChatBoostDefaults.date,
        source=ChatBoostDefaults.default_source,
    )


@pytest.fixture(scope="module")
def chat_boost():
    return ChatBoost(
        boost_id=ChatBoostDefaults.boost_id,
        add_date=ChatBoostDefaults.date,
        expiration_date=ChatBoostDefaults.date,
        source=ChatBoostDefaults.default_source,
    )


@pytest.fixture(scope="module")
def chat_boost_updated(chat_boost):
    return ChatBoostUpdated(
        chat=ChatBoostDefaults.chat,
        boost=chat_boost,
    )


def chat_boost_source_gift_code() -> ChatBoostSourceGiftCode:
    return ChatBoostSourceGiftCode(
        user=ChatBoostDefaults.user,
    )


def chat_boost_source_giveaway() -> ChatBoostSourceGiveaway:
    return ChatBoostSourceGiveaway(
        user=ChatBoostDefaults.user,
        giveaway_message_id=ChatBoostDefaults.giveaway_message_id,
        is_unclaimed=ChatBoostDefaults.is_unclaimed,
    )


def chat_boost_source_premium() -> ChatBoostSourcePremium:
    return ChatBoostSourcePremium(
        user=ChatBoostDefaults.user,
    )


@pytest.fixture(scope="module")
def user_chat_boosts(chat_boost):
    return UserChatBoosts(
        boosts=[chat_boost],
    )


@pytest.fixture()
def chat_boost_source(request: pytest.FixtureRequest) -> Callable[[], ChatBoostSource]:
    return request.param()


ignored = ["self", "api_kwargs"]


def make_json_dict(instance: ChatBoostSource, include_optional_args: bool = False) -> dict:
    """Used to make the json dict which we use for testing de_json. Similar to iter_args()"""
    json_dict = {"source": instance.source}
    sig = inspect.signature(instance.__class__.__init__)

    for param in sig.parameters.values():
        if param.name in ignored:  # ignore irrelevant params
            continue

        val = getattr(instance, param.name)
        if hasattr(val, "to_dict"):  # convert the user object or any future ones to dict.
            val = val.to_dict()
        json_dict[param.name] = val

    return json_dict


def iter_args(
    instance: ChatBoostSource, de_json_inst: ChatBoostSource, include_optional: bool = False
):
    """
    We accept both the regular instance and de_json created instance
