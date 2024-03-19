#!/usr/bin/env python

import pytest
from typing import Any, Dict, List, Optional, Type, Union

import telegram
from telegram.chat import Chat
from telegram.story import Story


class TestStory:
    """Test class for the `Story` class in the `telegram` module."""

    @pytest.fixture(scope="module")
    def story(self) -> Story:
        return Story(self.chat, self.id)

    @pytest.fixture(scope="module")
    def bot(self) -> telegram.Bot:
        # This fixture should be provided by the test suite.
        pass

    @pytest.mark.usefixtures("bot")
    def test_slot_behaviour(self, story: Story) -> None:
        slots = story.__slots__
        base_slots = slots[:1] + [s for s in slots[1:] if s not in ("api_kwargs",)]

        for attr in base_slots:
            assert getattr(story, attr, "err") != "err", f"got extra slot '{attr}'"

        args = get_args(type(story))
        all_slots = slots + args[1:]
        assert len(all_slots) == len(set(all_slots)), "duplicate slot"

    @pytest.mark.usefixtures("bot")
    def test_de_json(self, bot: telegram.Bot) -> None:
        json_dict = {"chat": self.chat.to_dict(), "id": self.id}
        story = Story.de_json(json_dict, bot)
        assert story.api_kwargs == {}
        assert story.chat == self.chat
        assert story.id == self.id
        assert isinstance(story, Story)
        assert Story.de_json(None, bot) is None

    @pytest.mark.usefixtures("bot")
    def test_to_dict(self, story: Story) -> None:
        story_dict = story.to_dict()
        assert story_dict["chat"] == self.chat.to_dict()
        assert story_dict["id"] == self.id

    @pytest.mark.usefixtures("bot")
    def test_equality(self) -> None:
        a = Story(Chat(1, ""), 0)
        b = Story(Chat(1, ""), 0)
        c = Story(Chat(1, ""), 1)
        d = Story(Chat(2, ""), 0)
        e = Chat(1, "")

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
