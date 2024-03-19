#!/usr/bin/env python

import pytest
from typing import Any, Dict, Tuple

from telegram import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


@pytest.fixture(scope="module")
def reply_keyboard_markup() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=TestReplyKeyboardMarkup.keyboard,
        resize_keyboard=TestReplyKeyboardMarkup.resize_keyboard,
        one_time_keyboard=TestReplyKeyboardMarkup.one_time_keyboard,
        selective=TestReplyKeyboardMarkup.selective,
        is_persistent=TestReplyKeyboardMarkup.is_persistent,
    )


class TestReplyKeyboardMarkup:
    keyboard = [[KeyboardButton("button1"), KeyboardButton("button2")]]
    resize_keyboard = True
    one_time_keyboard = True
    selective = True
    is_persistent = True

    @pytest.mark.unit
    def test_slot_behaviour(self, reply_keyboard_markup: ReplyKeyboardMarkup) -> None:
        """Test slot behaviour of ReplyKeyboardMarkup instance."""
        inst = reply_keyboard_markup
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    @pytest.mark.unit
    def test_expected_values(self, reply_keyboard_markup: ReplyKeyboardMarkup) -> None:
        """Test expected values of ReplyKeyboardMarkup instance."""
        assert isinstance(reply_keyboard_markup.keyboard, tuple)
        assert all(isinstance(row, tuple) for row in reply_keyboard_markup.keyboard)
        assert isinstance(reply_keyboard_markup.keyboard[0][0], KeyboardButton)
        assert isinstance(reply_keyboard_markup.keyboard[0][1], KeyboardButton)
        assert reply_keyboard_markup.resize_keyboard == self.resize_keyboard
        assert reply_keyboard_markup.one_time_keyboard == self.one_time_keyboard
        assert reply_keyboard_markup.selective == self.selective
        assert reply_keyboard_markup.is_persistent == self.is_persistent

    @pytest.mark.unit
    def test_to_dict(self, reply_keyboard_markup: ReplyKeyboardMarkup) -> None:
        """Test conversion to dictionary of ReplyKeyboardMarkup instance."""
        reply_keyboard_markup_dict = reply_keyboard_markup.to_dict()

        assert isinstance(reply_keyboard_markup_dict, dict)
        assert (
            reply_keyboard_markup_dict["keyboard"][0][0]
            == reply_keyboard_markup.keyboard[0][0].to_dict()
        )
        assert (
            reply_keyboard_markup_dict["keyboard"][0][1]
            == reply_keyboard_markup.keyboard[0][1].to_dict()
        )
        assert (
            reply_keyboard_markup_dict["resize_keyboard"] == reply_keyboard_markup.resize_keyboard
        )
        assert (
            reply_keyboard_markup_dict["one_time_keyboard"]
            == reply_keyboard_markup.one_time_keyboard
        )
        assert reply_keyboard_markup_dict["selective"] == reply_keyboard_markup.selective
        assert reply_keyboard_markup_dict["is_persistent"] == reply_keyboard_markup.is_persistent

    @pytest.mark.unit
    def test_equality(self) -> None:
        """Test equality of ReplyKeyboardMarkup instances."""
        a = ReplyKeyboardMarkup.from_column(["button1", "button2", "button3"])
        b = ReplyKeyboardMarkup.from_column(
            [KeyboardButton(text) for text in ["button1", "button2", "button3"]]
        )
        c = ReplyKeyboardMarkup.from_column(["button1", "button2"])
        d = ReplyKeyboardMarkup.from_column(["button1", "button2", "button3.1"])
        e = ReplyKeyboardMarkup(
            [
                ["button1", "button1"],
                ["button2"],
                ["button3.1"],
            ]
        )
        f = InlineKeyboardMarkup.from_column(["button1", "button2", "button3"])

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)

        assert a != f
        assert hash(a) != hash(f)

    @pytest.mark.unit
    def test_wrong_keyboard_inputs(self) -> None:
        """Test exception when wrong keyboard inputs are provided."""
        with pytest.raises(
            ValueError, match="should be a sequence of sequences of KeyboardButton instances"
        ):
            ReplyKeyboardMarkup([["button1"], 1])

        with pytest.raises(
            ValueError, match
