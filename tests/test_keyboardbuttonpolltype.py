#!/usr/bin/env python

import pytest
from telegram import KeyboardButtonPollType, Poll, PollType
from telegram.constants import PollType as PollTypeConstant


class TestKeyboardButtonPollType:
    """Tests for the KeyboardButtonPollType class."""

    @pytest.fixture(scope="module")
    def keyboard_button_poll_type(self):
        return KeyboardButtonPollType(self.type)

    type = Poll.QUIZ

    @pytest.mark.usefixtures("keyboard_button_poll_type")
    def test_slot_behaviour(self, keyboard_button_poll_type):
        inst = keyboard_button_poll_type
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    @pytest.mark.usefixtures("keyboard_button_poll_type")
    def test_to_dict(self, keyboard_button_poll_type):
        keyboard_button_poll_type_dict = keyboard_button_poll_type.to_dict()
        assert isinstance(keyboard_button_poll_type_dict, dict)
        assert keyboard_button_poll_type_dict["type"] == self.type

    @pytest.mark.parametrize(
        "poll_type_str, expected_result",
        [
            ("quiz", PollTypeConstant.QUIZ),
            ("regular", PollTypeConstant.REGULAR),
            ("unknown", "unknown"),
        ],
    )
    def test_type_enum_conversion(self, poll_type_str, expected_result):
        result = KeyboardButtonPollType(type=poll_type_str).type
        assert result == expected_result

    def test_equality(self):
        a = KeyboardButtonPollType(PollTypeConstant.QUIZ)
        b = KeyboardButtonPollType(PollTypeConstant.QUIZ)
        c = KeyboardButtonPollType(PollTypeConstant.REGULAR)

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a != c
        assert hash(a) != hash(c)
