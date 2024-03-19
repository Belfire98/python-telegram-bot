import asyncio
import pytest
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

from telegram import (
    Bot,
    CallbackQuery,
    Chat,
    ChosenInlineResult,
    InlineQuery,
    Message,
    PreCheckoutQuery,
    ShippingQuery,
    Update,
    User,
)
from telegram.ext import CallbackContext, ChosenInlineResultHandler, JobQueue
from tests.auxil.slots import mro_slots

T = TypeVar("T")

message: Message = Message(1, None, Chat(1, ""), from_user=User(1, "", False), text="Text")

params: List[Dict[str, Union[Message, CallbackQuery, InlineQuery, ShippingQuery, PreCheckoutQuery]]] = [
    {"message": message},
    {"edited_message": message},
    {"callback_query": CallbackQuery(1, User(1, "", False), "chat", message=message)},
    {"channel_post": message},
    {"edited_channel_post": message},
    {"inline_query": InlineQuery(1, User(1, "", False), "", "")},
    {"shipping_query": ShippingQuery("id", User(1, "", False), "", None)},
    {"pre_checkout_query": PreCheckoutQuery("id", User(1, "", False), "", 0, "")},
    {"callback_query": CallbackQuery(1, User(1, "", False), "chat")},
]

ids: List[str] = (
    "message",
    "edited_message",
    "callback_query",
    "channel_post",
    "edited_channel_post",
    "inline_query",
    "shipping_query",
    "pre_checkout_query",
    "callback_query_without_message",
)


@pytest.fixture(scope="class", params=params, ids=ids)
def false_update(request) -> Update:
    return Update(update_id=1, **request.param)


@pytest.fixture(scope="class")
def chosen_inline_result() -> Update:
    out = Update(
        1,
        chosen_inline_result=ChosenInlineResult("result_id", User(1, "test_user", False), "query"),
    )
    out._unfreeze()
    out.chosen_inline_result._unfreeze()
    return out


class TestChosenInlineResultHandler:
    """Tests for the `ChosenInlineResultHandler` class."""

    test_flag: bool = False

    @pytest.fixture(autouse=True)
    def _reset(self) -> None:
        self.test_flag = False

    def test_slot_behaviour(self) -> None:
        """Tests that the `ChosenInlineResultHandler` class has the correct slots."""
        handler = ChosenInlineResultHandler(self.callback_basic)
        for attr in handler.__slots__:
            assert getattr(handler, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(handler)) == len(set(mro_slots(handler))), "duplicate slot"

    def callback_basic(
        self, bot: Bot, update: Update, user_data:
