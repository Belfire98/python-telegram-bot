#!/usr/bin/env python

import pytest
from typing import Any, Callable, Dict, Optional

from telegram import (
    Bot,
    CallbackQuery,
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    Update,
    User,
)
from telegram.ext import ApplicationBuilder, CallbackContext, Job
from telegram.warnings import PTBUserWarning
from tests.auxil.slots import mro_slots

"""
CallbackContext.refresh_data is tested in TestBasePersistence
"""


class TestCallbackContext:
    @pytest.mark.usefixtures("app")
    def test_slot_behaviour(self, app: ApplicationBuilder) -> None:
        c = CallbackContext(app)
        for attr in c.__slots__:
            assert getattr(c, attr, "err") != "err", f"got extra slot '{attr}'"
        assert not c.__dict__, f"got missing slot(s): {c.__dict__}"
        assert len(mro_slots(c)) == len(set(mro_slots(c))), "duplicate slot"

    @pytest.mark.usefixtures("app")
    def test_from_job(self, app: ApplicationBuilder) -> None:
        job = app.job_queue.run_once(lambda x: x, 10)

        callback_context = CallbackContext.from_job(job, app)

        assert callback_context.job is job
        assert callback_context.chat_data is None
        assert callback_context.user_data is None
        assert callback_context.bot_data is app.bot_data
        assert callback_context.bot is app.bot
        assert callback_context.job_queue is app.job_queue
        assert callback_context.update_queue is app.update_queue

    @pytest.mark.usefixtures("bot", "app")
    def test_job_queue(self, bot: Bot, app: ApplicationBuilder, recwarn) -> None:
        expected_warning = (
            "No `JobQueue` set up. To use `JobQueue`, you must install PTB via "
            '`pip install "python-telegram-bot[job-queue]"`.'
        )

        callback_context = CallbackContext(app)
        assert callback_context.job_queue is app.job_queue
        app = ApplicationBuilder().job_queue(None).token(bot.token).build()
        callback_context = CallbackContext(app)
        assert callback_context.job_queue is None
        assert len(recwarn) == 1
        assert str(recwarn[0].message) == expected_warning
        assert recwarn[0].category is PTBUserWarning
        assert recwarn[0].filename == __file__, "wrong stacklevel"

    @pytest.mark.usefixtures("app")
    def test_from_update(self, app: ApplicationBuilder) -> None:
        update = Update(
            0, message=Message(0, None, Chat(1, "chat"), from_user=User(1, "user", False))
        )

        callback_context = CallbackContext.from_update(update, app)

        assert callback_context.chat_data == {}
        assert callback_context.user_data == {}
        assert callback_context.bot_data is app.bot_data
        assert callback_context.bot is app.bot
        assert callback_context.job_queue is app.job_queue
        assert callback_context.update_queue is app.update_queue

        callback_context_same_user_chat = CallbackContext.from_update(update, app)

        callback_context.bot_data["test"] = "bot"
        callback_context.chat_data["test"] = "chat"
        callback_context.user_data["test"] = "user"

        assert callback_context_same_user_chat.bot_data is callback_context.bot_data
        assert callback_context_same_user_chat.chat_data is callback_context.chat_data
        assert callback_context_same_user_chat.user_data is callback_context.user_data

        update_other_user_chat = Update(
            0, message=Message(0, None, Chat(2, "chat"), from_user=User(2, "user", False))
        )

        callback_context_other_user_chat = CallbackContext.from_update(update_other_user_chat, app)

        assert callback_context_other_user_chat.bot_data is callback_context.bot_data
        assert callback_context_other_user_chat.chat_data is not callback_context.chat_data
        assert callback_context_other_user_chat.user_data is not callback_context.user_data

    @pytest.mark.usefixtures("app")
    def test_from_update_not_update(self, app: ApplicationBuilder) -> None:
        callback_context = CallbackContext.from_update(None, app)

        assert callback_context.chat_data is None
        assert callback_context.user_data is None
        assert callback_context.bot_data is app.bot_data
        assert callback_context.bot is app.bot
        assert callback_context.job_queue is app.job_queue
        assert callback_context.update_queue is app.update_queue

        callback_context = CallbackContext.from_update("", app)

        assert callback_context.chat_data is None
        assert callback_context.user_data is None
        assert callback_context.bot_data is app.bot_data
        assert callback_context.bot is app.bot
        assert callback_context.job_queue is app.job_queue

