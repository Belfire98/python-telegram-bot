import pytest
from typing import Any, Dict
from unittest import TestCase

import telegram
from inspect import getslots


@pytest.fixture(scope="module")
def switch_inline_query_chosen_chat():
    return SwitchInlineQueryChosenChat(
        query="TestQuery",
        allow_user_chats=True,
        allow_bot_chats=True,
        allow_channel_chats=False,
        allow_group_chats=True,
    )


class TestSwitchInlineQueryChosenChatBase(TestCase):
    query: str = "query"
    allow_user_chats: bool = True
    allow_bot_chats: bool = True
    allow_channel_chats: bool = False
    allow_group_chats: bool = True


class TestSwitchInlineQueryChosenChat(TestSwitchInlineQueryChosenChatBase):
    def test_slot_behaviour(self, switch_inline_query_chosen_chat):
        inst = switch_inline_query_chosen_chat
        slots = getslots(inst)

        for attr in slots:
            value = getattr(inst, attr, "err")
            assert value != "err", f"got extra slot '{attr}'"

        assert len(slots) == len(set(slots)), "duplicate slot"

    def test_expected_values(self, switch_inline_query_chosen_chat):
        assert switch_inline_query_chosen_chat.query == self.query
        assert switch_inline_query_chosen_chat.allow_user_chats == self.allow_user_chats
        assert switch_inline_query_chosen_chat.allow_bot_chats == self.allow_bot_chats
        assert switch_inline_query_chosen_chat.allow_channel_chats == self.allow_channel_chats
        assert switch_inline_query_chosen_chat.allow_group_chats == self.allow_group_chats

    def test_to_dict(self, switch_inline_query_chosen_chat):
        siqcc = switch_inline_query_chosen_chat.to_dict()

        assert isinstance(siqcc, dict)
        assert siqcc["query"] == switch_inline_query_chosen_chat.query
        assert siqcc["allow_user_chats"] == switch_inline_query_chosen_chat.allow_user_chats
        assert siqcc["allow_bot_chats"] == switch_inline_query_chosen_chat.allow_bot_chats
        assert siqcc["allow_channel_chats"] == switch_inline_query_chosen_chat.allow_channel_chats
        assert siqcc["allow_group_chats"] == switch_inline_query_chosen_chat.allow_group_chats

    @pytest.mark.parametrize(
        "allow_group_chats, expected",
        [
            (False, False),
            (True, True),
        ],
    )
    def test_equality(self, allow_group_chats: bool, expected: bool, switch_inline_query_chosen_chat):
        siqcc = SwitchInlineQueryChosenChat(
            self.query,
            self.allow_user_chats,
            self.allow_bot_chats,
            allow_group_chats=allow_group_chats,
        )

        actual = siqcc == switch_inline_query_chosen_chat

        self.assertIs(actual, expected)
