#!/usr/bin/env python

import datetime as dtm
import pytest
from telegram import (
    User,
    VideoChatEnded,
    VideoChatParticipantsInvited,
    VideoChatScheduled,
    VideoChatStarted,
)
from telegram._utils.datetime import UTC, to_timestamp
from tests.auxil.slots import mro_slots


@pytest.fixture(scope="module")
def user1():
    return User(first_name="Misses Test", id=123, is_bot=False)


@pytest.fixture(scope="module")
def user2():
    return User(first_name="Mister Test", id=124, is_bot=False)


class TestVideoChatStartedWithoutRequest:
    @pytest.mark.usefixtures("user1", "user2")
    def test_slot_behaviour(self, user1):
        action = VideoChatStarted()
        for attr in action.__slots__:
            assert getattr(action, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(action)) == len(set(mro_slots(action))), "duplicate slot"

    def test_de_json(self):
        video_chat_started = VideoChatStarted.de_json({}, None)
        assert isinstance(video_chat_started, VideoChatStarted)

    def test_to_dict(self):
        video_chat_started = VideoChatStarted()
        video_chat_dict = video_chat_started.to_dict()
        assert isinstance(video_chat_dict, dict)


class TestVideoChatEndedWithoutRequest:
    duration: int

    @pytest.mark.usefixtures("user1", "user2")
    def test_slot_behaviour(self, user1):
        action = VideoChatEnded(8)
        for attr in action.__slots__:
            assert getattr(action, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(action)) == len(set(mro_slots(action))), "duplicate slot"

    def test_de_json(self):
        json_dict = {"duration": self.duration}
        video_chat_ended = VideoChatEnded.de_json(json_dict, None)
        assert video_chat_ended.duration == self.duration

    def test_to_dict(self):
        video_chat_ended = VideoChatEnded(self.duration)
        video_chat_dict = video_chat_ended.to_dict()
        assert isinstance(video_chat_dict, dict)

    def test_equality(self):
        a = VideoChatEnded(100)
        b = VideoChatEnded(100)
        c = VideoChatEnded(50)
        d = VideoChatStarted()

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)


class TestVideoChatParticipantsInvitedWithoutRequest:
    @pytest.mark.usefixtures("user1", "user2")
    def test_slot_behaviour(self, user1):
        action = VideoChatParticipantsInvited([user1])
        for attr in action.__slots__:
            assert getattr(action, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(action)) == len(set(mro_slots(action))), "duplicate slot"

    def test_de_json(self, user1, user2, bot):
        json_data = {"users": [user1.to_dict(), user2.to_dict()]}
        video_chat_participants = VideoChatParticipantsInvited.de_json(json_data, bot)
        assert isinstance(video_chat_participants.users, tuple)
        assert video_chat_participants.users[0] == user1
        assert video_chat_participants.users[1] == user2

    @pytest.mark.parametrize("use_users", [True, False])
    def test_to_dict(self, user1, user2, use_users, bot):
        video_chat_participants = VideoChatParticipantsInvited(
            [user1, user2] if use_users else ()
        )
        video_chat_dict = video_chat_participants.to_dict()

        assert isinstance(video_chat_dict, dict)
        if use_users:
            assert video_chat_dict["users"] == [user1.to_dict(), user2.to_dict()]
        else:
            assert video_chat_dict == {}

    def test_equality(self, user1, user2):
        a = VideoChatParticipantsInvited([user1])
        b = VideoChatParticipantsInvited([user1])
        c = VideoChatParticipantsInvited([user1, user2])
        d = VideoChatParticipantsInvited([])
        e = VideoChatStarted()

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)


