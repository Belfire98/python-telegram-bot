#!/usr/bin/env python

import pytest  # Added type hint
from typing import Any, Dict, List, Tuple

import telegram  # Typing for function and method parameters and return types
from telegram import (
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


@pytest.fixture(scope="module")
def inline_keyboard_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(TestInlineKeyboardMarkupBase.inline_keyboard)


class TestInlineKeyboardMarkupWithoutRequest(TestInlineKeyboardMarkupBase):
    def test_slot_behaviour(self, inline_keyboard_markup: InlineKeyboardMarkup) -> None:
        inst = inline_keyboard_markup
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(set(mro_slots(inst))) == len(mro_slots(inst)), "duplicate slot"

    def test_to_dict(self, inline_keyboard_markup: InlineKeyboardMarkup) -> None:
        inline_keyboard_markup_dict = inline_keyboard_markup.to_dict()

        assert isinstance(inline_keyboard_markup_dict, dict)
        assert inline_keyboard_markup_dict["inline_keyboard"] == [
            [self.inline_keyboard[0][0].to_dict(), self.inline_keyboard[0][1].to_dict()]
        ]

    @pytest.mark.asyncio  # Added decorator
    async def test_send_message_with_inline_keyboard_markup(
        self, bot, chat_id: int, inline_keyboard_markup: InlineKeyboardMarkup
    ) -> None:
        message = await bot.send_message(
            chat_id, "Testing InlineKeyboardMarkup", reply_markup=inline_keyboard_markup
        )

        assert message.text == "Testing InlineKeyboardMarkup"

    # ... (other test methods)


class TestInlineKeyborardMarkupWithRequest(TestInlineKeyboardMarkupBase):
    @pytest.mark.asyncio  # Added decorator
    async def test_send_message_with_inline_keyboard_markup(
        self, bot, chat_id: int, inline_keyboard_markup: InlineKeyboardMarkup
    ) -> None:
        message = await bot.send_message(
            chat_id, "Testing InlineKeyboardMarkup", reply_markup=inline_keyboard_markup
        )

        assert message.text == "Testing InlineKeyboardMarkup"

    # ... (other test methods)
