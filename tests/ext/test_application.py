import asyncio
import inspect
import logging
import os
import platform
import signal
import sys
import threading
import time
from collections import defaultdict
from queue import Queue
from random import randrange
from threading import Thread
from typing import Optional

import pytest

from telegram import Bot, Chat, Message, MessageEntity, User
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ApplicationHandlerStop,
    BaseHandler,
    CallbackContext,
    CommandHandler,
    ContextTypes,
    Defaults,
    JobQueue,
    MessageHandler,
    PicklePersistence,
    SimpleUpdateProcessor,
    TypeHandler,
    Updater,
    filters,
)
from telegram.warnings import PTBDeprecationWarning, PTBUserWarning
from tests.auxil.asyncio_helpers import call_after
from tests.auxil.build_messages import make_message_update
from tests.auxil.files import PROJECT_ROOT_PATH
from tests.auxil.networking import send_webhook_message
from tests.auxil.pytest_classes import make_bot
from tests.auxil.slots import mro_slots


class CustomContext(CallbackContext):
    pass


class TestApplication:
    """Test the integration of persistence into the application."""

    message_update = make_message_update(message="Text")
    received = None
    count = 0

    @pytest.fixture(autouse=True, name="reset")
    def _reset_fixture(self):
        self.reset()

    def reset(self):
        self.received = None
        self.count = 0

    async def error_handler_context(self, update, context):
        self.received = context.error.message

    async def error_handler_raise_error(self, update, context):
        raise Exception("Failing bigly")

    async def callback_increase_count(self, update, context):
        self.count += 1

    def callback_set_count(self, count, sleep: Optional[float] = None):
        async def callback(update, context):
            if sleep:
                await asyncio.sleep(sleep)
            self.count = count

        return callback

    def callback_raise_error(self, error_message: str):
        async def callback(update, context):
            raise TelegramError(error_message)

        return callback

    async def callback_received(self, update, context):
        self.received = update.message

    async def callback_context(self, update, context):
        if (
            isinstance(context, CallbackContext)
            and isinstance(context.bot, Bot)
            and isinstance(context.update_queue, Queue)
            and isinstance(context.job_queue, JobQueue)
            and isinstance(context.error, TelegramError)
        ):
            self.received = context.error.message

    async def test_slot_behaviour(self, one_time_bot):
        async with ApplicationBuilder().bot(one_time_bot).build() as app:
            for at in app.__slots__:
                attr = f"_Application{at}" if at.startswith("__") and not at.endswith("__") else at
                assert getattr(app, attr, "err") != "err", f"got extra slot '{attr}'"
            assert len(mro_slots(app)) == len(set(mro_slots(app))), "duplicate slot"

    def test_manual_init_warning(self, recwarn, updater):
        Application(
            bot=None,
            update_queue=None,
            job_queue=None,
            persistence=None,
            context_types=ContextTypes(),
            updater=updater,
            update_processor=False,
            post_init=None,
            post_shutdown=None,
            post_stop=None,
        )
        assert len(recwarn) == 1
        assert (
            str(recwarn[-1].message)
            == "`Application` instances should be built via the `ApplicationBuilder`."
        )
        assert recwarn[0].category is PTBUserWarning
        assert recwarn[0].filename == __file__, "stacklevel is incorrect!"

    @pytest.mark.filterwarnings("ignore: `Application` instances should")
    def test_init(self, one_time_bot):
        update_queue = asyncio.Queue()
        job_queue = JobQueue()
        persistence = PicklePersistence("file_path")
        context_types = ContextTypes()
        update_processor = SimpleUpdateProcessor(1)
        updater = Updater(bot=one_time_bot, update_queue=update_queue)

        async def post_init(application: Application) -> None:
            pass

        async def post_shutdown(application: Application) -> None:
            pass

        async def post_stop(application: Application) -> None:
            pass

        app = Application(
            bot=one_time_bot,
            update_queue=update_queue,
            job_queue=job_queue,
            persistence=persistence,
            context_types=context_types,
            updater=updater,
            update_processor=update_processor,
            post_init=post_init,
            post_shutdown=post_shutdown,
            post_stop=post_stop,
        )
        assert app.bot is one_time_bot
        assert app.update_queue is update_queue
        assert app.job_queue is job_queue
        assert app.persistence is persistence
        assert app.context_types is context_types
        assert app.updater is updater
        assert app.update_queue is updater.update_queue
        assert app.bot is updater.bot
        assert app.update_processor is update_processor
        assert app.post_init is post_init
        assert app.post_shutdown is post_shutdown
        assert app.post_stop is post_stop

        # These should be done by the
