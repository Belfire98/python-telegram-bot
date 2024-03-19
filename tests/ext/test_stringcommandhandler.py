#!/usr/bin/env python

import asyncio
import pytest
from typing import Any, Callable, Coroutine, Dict, List, Optional, Union

import telegram
from telegram.ext import CallbackContext, JobQueue, StringCommandHandler
from tests.auxil.slots import mro_slots

message = telegram.Message(1, None, telegram.Chat(1, ""), from_user=telegram.User(1, "", False), text="Text")

params = [
    {"message": message},
    {"edited_message": message},
    {"callback_query": telegram.CallbackQuery(1, telegram.User(1, "", False), "chat", message=message)},
    {"channel_post": message},
    {"edited_channel_post": message},
    {"inline_query": telegram.InlineQuery(1, telegram.User(1, "", False), "", "")},
    {"chosen_inline_result": telegram.ChosenInlineResult("id", telegram.User(1, "", False), "")},
    {"shipping_query": telegram.ShippingQuery("id", telegram.User(1, "", False), "", None)},
    {"pre_checkout_query": telegram.PreCheckoutQuery("id", telegram.User(1, "", False), "", 0, "")},
    {"callback_query": telegram.CallbackQuery(1, telegram.User(1, "", False), "chat")},
]

ids = (
    "message",
    "edited_message",
    "callback_query",
    "channel_post",
    "edited_channel_post",
    "inline_query",
    "chosen_inline_result",
    "shipping_query",
    "pre_checkout_query",
    "callback_query_without_message",
)

test_flag: bool = False

@pytest.fixture(scope="class", params=params, ids=ids)
def false_update(request):
    return telegram.Update(update_id=1, **request.param)


class TestStringCommandHandler:

    def test_slot_behaviour(self):
        inst = StringCommandHandler("sleepy", self.callback)
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    @pytest.fixture(autouse=True)
    def _reset(self):
        self.test_flag = False

    @pytest.mark.asyncio
    async def callback(self, update: telegram.Update, context: CallbackContext, request: pytest.FixtureRequest) -> None:
        self.test_flag = (
            isinstance(context, CallbackContext)
            and isinstance(context.bot, telegram.Bot)
            and isinstance(update, str)
            and isinstance(context.update_queue, asyncio.Queue)
            and isinstance(context.job_queue, JobQueue)
            and context.user_data is None
            and context.chat_data is None
            and isinstance(context.bot_data, dict)
        )

    @pytest.mark.asyncio
    async def callback_args(self, update: telegram.Update, context: CallbackContext, request: pytest.FixtureRequest) -> None:
        self.test_flag = context.args == ["one", "two"]

    @pytest.mark.asyncio
    def test_other_update_types(self, false_update: telegram.Update) -> None:
        handler = StringCommandHandler("test", self.callback)
        yield handler.check_update(false_update)
        assert not self.test_flag

    @pytest.mark.asyncio
    async def test_context(self, app: Any) -> None:
        handler = StringCommandHandler("test", self.callback)
        app.add_handler(handler)

        async with app:
            await app.process_update("/test")
        assert self.test_flag

    @pytest.mark.asyncio
    async def test_context_args(self, app: Any) -> None:
        handler = StringCommandHandler("test", self.callback_args)
        app.add_handler(handler)

        async with app:
            await app.process_update("/test")
            assert not self.test_flag

            await app.process_update("/test one two")
            assert self.test_flag
