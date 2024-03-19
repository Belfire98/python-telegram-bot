#!/usr/bin/env python

import datetime
import inspect
from copy import deepcopy
from typing import Any, Dict, List, Optional, Type, Union

import pytest
from telegram import (
    Chat,
    Dice,
    MessageOrigin,
    MessageOriginChannel,
    MessageOriginChat,
    MessageOriginHiddenUser,
    MessageOriginUser,
    User,
)
from telegram._utils.datetime import UTC, to_timestamp
from tests.auxil.slots import mro_slots

Ignored = ["self", "api_kwargs"]


class MODefaults:
    date: datetime.datetime = to_timestamp(datetime.datetime.utcnow())  # type: datetime.datetime
    chat = Chat(1, Chat.CHANNEL)  # type: Chat
    message_id = 123  # type: int
    author_signautre = "PTB"  # type: str
    sender_chat = Chat(1, Chat.CHANNEL)  # type: Chat
    sender_user_name = "PTB"  # type: str
    sender_user = User(1, "user", False)  # type: User


def message_origin_channel() -> MessageOriginChannel:
    return MessageOriginChannel(
        MODefaults.date, MODefaults.chat, MODefaults.message_id, MODefaults.author_signautre
    )


def message_origin_chat() -> MessageOriginChat:
    return MessageOriginChat(
        MODefaults.date,
        MODefaults.sender_chat,
        MODefaults.author_signautre,
    )


def message_origin_hidden_user() -> MessageOriginHiddenUser:
    return MessageOriginHiddenUser(MODefaults.date, MODefaults.sender_user_name)


def message_origin_user() -> MessageOriginUser:
    return MessageOriginUser(MODefaults.date, MODefaults.sender_user)


def make_json_dict(
    instance: MessageOrigin, include_optional_args: bool = False
) -> Dict[str, Union[str, int, datetime.datetime, Dict[str, Any]]]:
    """Used to make the json dict which we use for testing de_json. Similar to iter_args()"""
    json_dict = {"type": instance.type}
    sig = inspect.signature(instance.__class__.__init__)

    for param in sig.parameters.values():
        if param.name in Ignored:  # ignore irrelevant params
            continue

        val = getattr(instance, param.name)
        # Compulsory args-
        if param.default is inspect.Parameter.empty:
            if hasattr(val, "to_dict"):  # convert the user object or any future ones to dict.
                val = val.to_dict()
            json_dict[param.name] = val

        # If we want to test all args (for de_json)-
        elif param.default is not inspect.Parameter.empty and include_optional_args:
            json_dict[param.name] = val
    return json_dict


def iter_args(
    instance: MessageOrigin, de_json_inst: MessageOrigin, include_optional: bool = False
) -> List[Tuple[Any, Any]]:
    """
    We accept both the regular instance and de_json created instance and iterate over them for
    easy one line testing later one.
    """
    yield instance.type, de_json_inst.type  # yield this here cause it's not available in sig.

    sig = inspect.signature(instance.__class__.__init__)
    for param in sig.parameters.values():
        if param.name in Ignored:
            continue
        inst_at, json_at = getattr(instance, param.name), getattr(de_json_inst, param.name)
        if isinstance(json_at, datetime.datetime):  # Convert datetime to int
            json_at = to_timestamp(json_at)
        if (
            param.default is not inspect.Parameter.empty and include_optional
        ) or param.default is inspect.Parameter.empty:
            yield inst_at, json_at


@pytest.fixture()
def message_origin_type(request) -> Type[MessageOrigin]:
    return request.param()


@pytest.mark.parametrize(
    "message_origin_type",
    [
        message_origin_channel,
        message_origin_chat,
        message_origin_hidden_user,
        message_origin_user,
    ],
    indirect=True,
)
class TestMessageOriginTypesWithoutRequest:
    def test_slot_behaviour(self, message_origin_type):
        inst = message_origin_type()
        for attr in message_origin_type().__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert (
            len(mro_slots(inst)) == len(set(mro_slots(inst)))
        ), "duplicate slot"

    def test_de_json_required_args(
        self, bot: "telegram.Bot", message_origin_type: Type[MessageOrigin]
    ):
        cls = message_origin_type
        assert cls.de_json({}, bot) is None

        json_dict = make_json_dict(message_origin_type())
        const_message_origin = MessageOrigin.de_json(json_dict, bot)
        assert const_message_origin.api_kwargs == {}

        assert isinstance(const_message_origin, MessageOrigin)
        assert isinstance(const_message_origin, cls)
        for msg_origin_type_at, const_msg_origin_at in iter_args(
            message_origin_type(), const_message_origin
        ):
            assert msg_origin_
