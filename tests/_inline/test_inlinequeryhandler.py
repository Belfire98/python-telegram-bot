#!/usr/bin/env python

import asyncio
import pytest
from typing import Any, Dict, List, Optional

import telegram
from telegram.ext import CallbackContext, InlineQueryHandler

message = telegram.Message(1, None, telegram.Chat(1, ""), from_user=telegram.User(1, "", False), text="Text")

params: List[Dict[str, Any]] = [
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

ids: List[str] = (
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
def false_update(request) -> telegram.Update:
    return telegram.Update(update_id=2, **request.param)


@pytest.fixture()
def inline_query(bot) -> telegram.Update:
    update = telegram.Update(
        0,
        inline_query=telegram.InlineQuery(
            "id",
            telegram.User(2, "test user", False),
            "test query",
            offset="22",
            location=telegram.Location(latitude=-23.691288, longitude=-46.788279),
        ),
    )
    update._unfreeze()
    update.inline_query._unfreeze()
    return update


class TestInlineQueryHandler:
    test_flag: bool = False

    def test_slot_behaviour(self):
        handler = InlineQueryHandler(self.callback)
        for attr in handler.__slots__:
            assert getattr(handler, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(handler)) == len(set(mro_slots(handler))), "duplicate slot"

    def _reset(self):
        self.test_flag = False

    @pytest.fixture(autouse=True)
    def reset(self):
        self._reset()

    async def callback(self, update: telegram.Update, context: CallbackContext) -> None:
        self.test_flag = (
            isinstance(context, CallbackContext)
            and isinstance(context.bot, telegram.Bot)
            and isinstance(update, telegram.Update)
            and isinstance(context.update_queue, asyncio.Queue)
            and isinstance(context.job_queue, telegram.JobQueue)
            and isinstance(context.user_data, dict)
            and context.chat_data is None
            and isinstance(context.bot_data, dict)
            and isinstance(update.inline_query, telegram.InlineQuery)
        )

    def callback_pattern(self, update: telegram.Update, context: CallbackContext) -> None:
        if context.matches[0].groups():
            self.test_flag = context.matches[0].groups() == ("t", " query")
        if context.matches[0].groupdict():
            self.test_flag = context.matches[0].groupdict() == {"begin": "t", "end": " query"}

    def test_other_update_types(self, false_update: telegram.Update) -> None:
        handler = InlineQueryHandler(self.callback)
        assert not handler.check_update(false_update)

    async def test_context(self, app, inline_query: telegram.Update) -> None:
        handler = InlineQueryHandler(self.callback)
        app.add_handler(handler)

        async with app:
            await app.process_update(inline_query)
        assert self.test_flag

    async def test_context_pattern(self, app, inline_query: telegram.Update) -> None:
        handler = InlineQueryHandler(self.callback_pattern, pattern=r"(?P<begin>.*)est(?P<end>.*)")
        app.add_handler(handler)

        async with app:
            await app.process_update(inline_query)
            assert self.test_flag

            app.remove_handler(handler)
            handler = InlineQueryHandler(self.callback_pattern, pattern=r"(t)est(.*)")
            app.add_handler(handler)

            await app.process_update(inline_query)
            assert self.test_flag

            update = telegram.Update(
                update_id=0, inline_query=telegram.InlineQuery(id="id", from_user=None, query="", offset="")
            )
            update.inline_query._unfreeze()
            assert not handler.check_update(update)
            update.inline_query.query = "not_a_match"
            assert not handler.check_update
