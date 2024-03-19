import time
from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from telegram import CallbackQuery, Chat, InlineKeyboardButton, InlineKeyboardMarkup, Message, User
from telegram._utils.datetime import UTC
from telegram.ext import ExtBot
from telegram.ext._callbackdatacache import CallbackDataCache, InvalidCallbackData, _KeyboardData

pytestmark = [pytest.mark.usefixtures("callback_data_cache")]


@pytest.fixture()
def tz_bot():
    bot = ExtBot(token="TOKEN")
    bot.defaults.tzinfo = timezone.utc
    return bot


class TestCallbackDataCache:
    """Tests for `CallbackDataCache` class."""

    @pytest.mark.parametrize(
        "maxsize,expected_maxsize", [(1, 1), (5, 5), (2048, 2048), (0, 1024)]
    )
    def test_init_maxsize(self, callback_data_cache, maxsize, expected_maxsize):
        """Test that `maxsize` is set correctly in `CallbackDataCache` constructor."""
        cdc = CallbackDataCache(bot=callback_data_cache.bot, maxsize=maxsize)
        assert cdc.maxsize == expected_maxsize

    @pytest.mark.timeout(1)
    @pytest.mark.filterwarnings("ignore:The optional dependency")
    def test_init(self, callback_data_cache):
        """Test that `RuntimeError` is raised when `python-telegram-bot[callback-data]` is not installed."""
        with pytest.raises(RuntimeError, match=r"python-telegram-bot\[callback-data\]"):
            CallbackDataCache(bot=callback_data_cache.bot)

    @pytest.mark.timeout(1)
    @pytest.mark.filterwarnings("ignore:The optional dependency")
    def test_bot_init(self):
        """Test that `bot.callback_data_cache` is `None` when `arbitrary_callback_data` is not set."""
        bot = ExtBot(token="TOKEN")
        assert bot.callback_data_cache is None

        with pytest.raises(RuntimeError, match=r"python-telegram-bot\[callback-data\]"):
            ExtBot(token="TOKEN", arbitrary_callback_data=True)

    def test_slot_behaviour(self, callback_data_cache):
        """Test that `__slots__` are used correctly in `CallbackDataCache` and its subclasses."""
        for attr in callback_data_cache.__slots__:
            at = (
                f"_CallbackDataCache{attr}"
                if attr.startswith("__") and not attr.endswith("__")
                else attr
            )
            assert getattr(callback_data_cache, at, "err") != "err", f"got extra slot '{at}'"
        assert len(mro_slots(callback_data_cache)) == len(
            set(mro_slots(callback_data_cache))
        ), "duplicate slot"

    @pytest.mark.parametrize(
        "data,message,invalid,expected_data,expected_message,expected_invalid",
        [
            (True, True, False, "some data 1", reply_markup, False),
            (False, True, False, None, reply_markup, False),
            (True, False, False, "some data 1", None, False),
            (False, False, False, None, None, False),
            (True, True, True, InvalidCallbackData(), None, True),
            (False, True, True, InvalidCallbackData(), None, True),
            (True, False, True, InvalidCallbackData(), None, True),
            (False, False, True, InvalidCallbackData(), None, True),
        ],
    )
    def test_process_callback_query(
        self,
        callback_data_cache,
        data,
        message,
        invalid,
        expected_data,
        expected_message,
        expected_invalid,
    ):
        """Test that `process_callback_query` method works correctly."""
        reply_markup = InlineKeyboardMarkup.from_row(
            [
                InlineKeyboardButton("non-changing", url="https://ptb.org"),
                InlineKeyboardButton("changing", callback_data="some data 1"),
                InlineKeyboardButton("changing", callback_data="some data 2"),
            ]
        )

        out = callback_data_cache.process_keyboard(reply_markup)
        if invalid:
            callback_data_cache.clear_callback_data()

        chat = Chat(1, "private")
        effective_message = Message(
            message_id=1,
            date=datetime.now(),
            chat=chat,
            reply_markup=out,
            _unfreeze=lambda: None,
        )
        effective_message.reply_to_message = deepcopy(effective_message)
        effective_message.pinned_message = deepcopy(effective_message)
        cq_id = uuid4().hex
        callback_
