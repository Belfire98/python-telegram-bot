import time

import pytest
from typing import Any, Callable, List, Optional, TypeVar

import telegram
from telegram._utils.datetime import from_timestamp
from telegram.ext import CallbackContext
from tests.auxil.slots import mro_slots
from tests.test_update import params as all_params

T = TypeVar("T")


class TestChatBoostHandler:
    """Test class for ChatBoostHandler."""

    def __init__(self):
        """Initialize the test class."""
        self.test_flag = False

    def test_slot_behaviour(self):
        """Test slot behaviour."""
        action = ChatBoostHandler(self.cb_chat_boost_removed)
        for attr in action.__slots__:
            assert getattr(action, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(action)) == len(set(mro_slots(action))), "duplicate slot"

    @pytest.fixture(autouse=True)
    def _reset(self):
        """Reset the test flag."""
        self.test_flag = False

    async def cb_chat_boost_updated(self, update: telegram.Update, context: CallbackContext):
        """Callback function for chat boost updated."""
        self.test_flag = (
            isinstance(context, CallbackContext)
            and isinstance(update.chat_boost, telegram.ChatBoostUpdated)
            and not isinstance(update.removed_chat_boost, telegram.ChatBoostRemoved)
        )

    async def cb_chat_boost_removed(self, update: telegram.Update, context: CallbackContext):
        """Callback function for chat boost removed."""
        self.test_flag = (
            isinstance(context, CallbackContext)
            and isinstance(update.removed_chat_boost, telegram.ChatBoostRemoved)
            and not isinstance(update.chat_boost, telegram.ChatBoostUpdated)
        )

    async def cb_chat_boost_any(self, update: telegram.Update, context: CallbackContext):
        """Callback function for any chat boost."""
        self.test_flag = isinstance(context, CallbackContext) and (
            isinstance(update.removed_chat_boost, telegram.ChatBoostRemoved)
            or isinstance(update.chat_boost, telegram.ChatBoostUpdated)
        )

    @pytest.mark.parametrize(
        argnames=["allowed_types", "cb", "expected"],
        argvalues=[
            (ChatBoostHandler.CHAT_BOOST, "cb_chat_boost_updated", (True, False)),
            (ChatBoostHandler.REMOVED_CHAT_BOOST, "cb_chat_boost_removed", (False, True)),
            (ChatBoostHandler.ANY_CHAT_BOOST, "cb_chat_boost_any", (True, True)),
        ],
        ids=["CHAT_BOOST", "REMOVED_CHAT_BOOST", "ANY_CHAT_MEMBER"],
    )
    async def test_chat_boost_types(
        self, app: Any, cb: Callable, expected: T, allowed_types: Optional[T]
    ):
        """Test chat boost types."""
        result_1, result_2 = expected

        update_type, other = chat_boost_updated_update(), removed_chat_boost_update()

        handler = ChatBoostHandler(getattr(self, cb), chat_boost_types=allowed_types)
        app.add_handler(handler)

        async with app:
            assert handler.check_update(update_type) is result_1
            await app.process_update(update_type)
            assert self.test_flag is result_1

            self.test_flag = False

            assert handler.check_update(other) is result_2
            await app.process_update(other)
            assert self.test_flag is result_2

    def test_other_update_types(self, false_update: telegram.Update):
        """Test other update types."""
        handler = ChatBoostHandler(self.cb_chat_boost_removed)
        assert not handler.check_update(false_update)
        assert not handler.check_update(True)

    async def test_context(self, app: Any):
        """Test context."""
        handler = ChatBoostHandler(self.cb_chat_boost_updated)
        app.add_handler(handler)

        async with app:
            await app.process_update(chat_boost_updated_update())
            assert self.test_flag

    def test_with_chat_id(self):
        """Test with chat ID."""
        update
