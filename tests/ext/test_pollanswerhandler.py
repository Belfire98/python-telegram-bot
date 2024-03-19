#!/usr/bin/env python

import asyncio
import pytest
from typing import Any, Callable, Dict, List, Optional

import telegram
from telegram.ext import CallbackContext, JobQueue, PollAnswerHandler
from tests.auxil.slots import mro_slots

message = telegram.Message(1, None, telegram.Chat(1, ""), from_user=telegram.User(1, "", False), text="Text")

params = [
    {"message": message},
    {"edited_message": message},
    {"callback_query": telegram.CallbackQuery(1, telegram.User(1, "", False), "chat", message=message)},
    {"channel_post": message},
    {"edited_channel_post": message},
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
    "chosen_inline_result",
    "shipping_query",
    "pre_checkout_query",
    "callback_query_without_message",
)


@pytest.fixture(scope="class", params=params, ids=ids)
def false_update(request):
    return telegram.Update(update_id=2, **request.param)


@pytest.fixture()
def poll_answer() -> telegram.Update:
    return telegram.Update(
        0,
        poll_answer=telegram.PollAnswer(1, [0, 1], telegram.User(2, "test user", False), telegram.Chat(1, "")),
    )


class TestPollAnswerHandler:
    test_flag: bool

    def test_slot_behaviour(self, handler: PollAnswerHandler):
        for attr in handler.__slots__:
            assert getattr(handler, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(handler)) == len(set(mro_slots(handler))), "duplicate slot"

    @pytest.fixture(autouse=True)
    def _reset(self):
        self.test_flag = False

    async def callback(self, update: telegram.Update, context: CallbackContext):
        self.test_flag = (
            isinstance(context, CallbackContext)
            and isinstance(context.bot, telegram.Bot)
            and isinstance(update, telegram.Update)
            and isinstance(context.update_queue, asyncio.Queue)
            and isinstance(context.job_queue, JobQueue)
            and isinstance(context.user_data, dict)
            and context.chat_data is None
            and isinstance(context.bot_data, dict)
            and isinstance(update.poll_answer, telegram.PollAnswer)
        )

    def test_other_update_types(self, false_update: telegram.Update):
        handler = PollAnswerHandler(self.callback)
        assert not handler.check_update(false_update)

    async def test_context(self, app, poll_answer: telegram.Update):
        handler = PollAnswerHandler(self.callback)
        app.add_handler(handler)

        async with app:
            await app.process_update(poll_answer)
        assert self.test_flag
