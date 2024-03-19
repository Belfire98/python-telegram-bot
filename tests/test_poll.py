#!/usr/bin/env python

import datetime
import pytest
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Type, Union
from unittest.case import TestCase
from unittest.mock import Mock

import telegram
from telegram._utils.datetime import to_timestamp
from telegram.constants import PollType
from telegram.error import TelegramError
from telegram.poll import Poll, PollAnswer, PollOption
from telegram.test.base import unittest_run_loop
from telegram.test.auxil.slots import mro_slots
from tests.auxil.slots import SlotsTestMixin


class TestPollOptionBase(NamedTuple):
    text: str
    voter_count: int


class TestPollOptionWithoutRequest(SlotsTestMixin, TestCase):
    poll_option_class = PollOption

    def setUp(self) -> None:
        self.poll_option = self.poll_option_class(
            text=self.text, voter_count=self.voter_count
        )
        self.poll_option._unfreeze()

    def test_slot_behaviour(self) -> None:
        for attr in self.poll_option.__slots__:
            value = getattr(self.poll_option, attr, "err")
            self.assertIsInstance(value, str) and value != "err"
        self.assertEqual(
            len(mro_slots(self.poll_option)),
            len(set(mro_slots(self.poll_option))),
            "duplicate slot",
        )

    def test_de_json(self) -> None:
        json_dict = {"text": self.text, "voter_count": self.voter_count}
        poll_option = self.poll_option_class.de_json(json_dict, None)
        self.assertDictEqual(poll_option.api_kwargs, {})

        self.assertEqual(poll_option.text, self.text)
        self.assertEqual(poll_option.voter_count, self.voter_count)

    def test_to_dict(self) -> None:
        poll_option_dict = self.poll_option.to_dict()

        self.assertIsInstance(poll_option_dict, dict)
        self.assertEqual(poll_option_dict["text"], self.poll_option.text)
        self.assertEqual(poll_option_dict["voter_count"], self.poll_option.voter_count)

    def test_equality(self) -> None:
        a = self.poll_option_class(text="text", voter_count=1)
        b = self.poll_option_class(text="text", voter_count=1)
        c = self.poll_option_class(text="text_1", voter_count=1)
        d = self.poll_option_class(text="text", voter_count=2)
        e = Poll(123, "question", [a, b], 1, False, True, PollType.REGULAR, True)

        self.assertTrue(a == b)
        self.assertTrue(hash(a) == hash(b))

        self.assertFalse(a == c)
        self.assertFalse(hash(a) == hash(c))

        self.assertFalse(a == d)
        self.assertFalse(hash(a) == hash(d))

        self.assertFalse(a == e)
        self.assertFalse(hash(a) == hash(e))


class TestPollAnswerBase(NamedTuple):
    poll_id: str
    option_ids: List[int]
    user: telegram.User
    voter_chat: telegram.Chat


class TestPollAnswerWithoutRequest(SlotsTestMixin, TestCase):
    poll_answer_class = PollAnswer

    def setUp(self) -> None:
        self.poll_answer = self.poll_answer_class(
            self.poll_id, self.option_ids, self.user, self.voter_chat
        )
        self.poll_answer._unfreeze()

    def test_de_json(self) -> None:
        json_dict = {
            "poll_id": self.poll_id,
            "option_ids": self.option_ids,
            "user": self.user.to_dict(),
            "voter_chat": self.voter_chat.to_dict(),
        }
        poll_answer = self.poll_answer_class.de_json(json_dict, None)
        self.assertDictEqual(poll_answer.api_kwargs, {})

        self.assertEqual(poll_answer.poll_id, self.poll_id)
        self.assertListEqual(poll_answer.option_ids, self.option_ids)
        self.assertIsInstance(poll
