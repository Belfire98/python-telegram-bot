#!/usr/bin/env python

import asyncio
import datetime
from typing import Any

import pytest
from telegram import (
    Bot,
    CallbackQuery,
    Chat,
    ChosenInlineResult,
    Message,
    MessageReactionCountUpdated,
    MessageReactionUpdated,
    PreCheckoutQuery,
    ReactionCount,
    ReactionTypeEmoji,
    ShippingQuery,
    Update,
    User,
)
from telegram._utils.datetime import UTC
from telegram.ext import CallbackContext, JobQueue, MessageReactionHandler
from tests.auxil.slots import mro_slots

import pytest_asyncio

message: Message = Message(1, None, Chat(1, ""), from_user=User(1, "", False), text="Text")

params = [
    {"message": message},
    {"edited_message": message},
    {"callback_query": CallbackQuery(1, User(1, "", False), "chat", message=message)},
    {"channel_post": message},
    {"edited_channel_post": message},
    {"chosen_inline_result": ChosenInlineResult("id", User(1, "", False), "")},
    {"shipping_query": ShippingQuery("id", User(1, "", False), "", None)},
    {"pre_checkout_query": PreCheckoutQuery("id", User(1, "", False), "", 0, "")},
    {"callback_query": CallbackQuery(1, User(1, "", False), "chat")},
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
    return Update(update_id=2, **request.param)


@pytest.fixture(scope="class")
def time():
    return datetime.datetime.now(tz=UTC)


@pytest.fixture(scope="class")
def bot():
    return Bot(token="TOKEN")


@pytest.fixture(scope="class")
def message_reaction_updated(time, bot):
    mr = MessageReactionUpdated(
        chat=Chat(1, Chat.SUPERGROUP),
        message_id=1,
        date=time,
        old_reaction=[ReactionTypeEmoji("👍")],
        new_reaction=[ReactionTypeEmoji("👎")],
        user=User(1, "user_a", False),
        actor_chat=Chat(2, Chat.SUPERGROUP),
    )
    mr.set_bot(bot)
    mr._unfreeze()
    mr.chat._unfreeze()
    mr.user._unfreeze()
    return mr


@pytest.fixture(scope="class")
def message_reaction_count_updated(time, bot):
    mr = MessageReactionCountUpdated(
        chat=Chat(1, Chat.SUPERGROUP),
        message_id=1,
        date=time,
        reactions=[
            ReactionCount(ReactionTypeEmoji("👍"), 1),
            ReactionCount(ReactionTypeEmoji("👎"), 1),
        ],
    )
    mr.set_bot(bot)
    mr._unfreeze()
    mr.chat._unfreeze()
    return mr


class TestMessageReactionHandlerWithMessageReactionUpdated:
    @pytest.mark.asyncio
    async def test_slot_behaviour(self):
        action = MessageReactionHandler(self.callback)
        for attr in action.__slots__:
            assert getattr(action, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(action)) == len(set(mro_slots(action))), "duplicate slot"

    @pytest.fixture(autouse=True)
    def _reset(self):
        self.test_flag = False

    @pytest.mark.asyncio
    async def callback(self, update: Update, context: CallbackContext):
        self.test_flag = (
            isinstance(context, CallbackContext)
            and isinstance(context.bot, Bot)
            and isinstance(update, Update)
            and isinstance(context.update_queue, asyncio.Queue)
            and isinstance(context.job_queue, JobQueue)
            and isinstance(context.user_data, dict if update.effective_user else type(None))
            and isinstance(context.chat_data, dict)
            and isinstance(context.bot_data, dict)
            and (
                isinstance(
                    update.message_reaction,
                    MessageReactionUpdated,
                )
                or isinstance(update.message_reaction_count, MessageReactionCountUpdated)
            )
        )

    @pytest.mark.asyncio
    async def test_other_update_types(self, false_update):
        handler = MessageReactionHandler(self.callback)
        assert not handler.check_update(false_update)
        assert not handler.check_update(True)

    @pytest.mark.asyncio
    async def test_context(self, app, message_reaction_update, message_reaction_count_update):
        handler = MessageReactionHandler(callback=self.callback)
        app.add_handler(handler)

        async with app:
            assert handler.check_update(
