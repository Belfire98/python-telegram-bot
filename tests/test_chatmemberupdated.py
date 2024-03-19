#!/usr/bin/env python

import datetime
import inspect
from typing import Any, Dict, TypeVar, Union

import pytest
from telegram import (
    Chat,
    ChatInviteLink,
    ChatMember,
    ChatMemberAdministrator,
    ChatMemberBanned,
    ChatMemberOwner,
    ChatMemberUpdated,
    User,
)
from telegram._utils.datetime import UTC, to_timestamp
from tests.auxil.slots import mro_slots

T = TypeVar("T")


@pytest.fixture(scope="module")
def user() -> User:
    return User(1, "First name", False)


@pytest.fixture(scope="module")
def chat() -> Chat:
    return Chat(1, Chat.SUPERGROUP, "Chat")


@pytest.fixture(scope="module")
def old_chat_member(user: User) -> ChatMember:
    return ChatMember(user, TestChatMemberUpdatedBase.old_status)


@pytest.fixture(scope="module")
def new_chat_member(user: User) -> ChatMemberAdministrator:
    return ChatMemberAdministrator(
        user,
        TestChatMemberUpdatedBase.new_status,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        can_post_stories=True,
        can_edit_stories=True,
        can_delete_stories=True,
    )


@pytest.fixture(scope="module")
def time() -> datetime.datetime:
    return datetime.datetime.now(tz=UTC)


@pytest.fixture(scope="module")
def invite_link(user: User) -> ChatInviteLink:
    return ChatInviteLink("link", user, False, True, True)


@pytest.fixture(scope="module")
def chat_member_updated(
    user: User,
    chat: Chat,
    old_chat_member: ChatMember,
    new_chat_member: ChatMemberAdministrator,
    invite_link: ChatInviteLink,
    time: datetime.datetime,
) -> ChatMemberUpdated:
    return ChatMemberUpdated(chat, user, time, old_chat_member, new_chat_member, invite_link, True)


class TestChatMemberUpdatedBase:
    old_status: int = ChatMember.MEMBER
    new_status: int = ChatMember.ADMINISTRATOR


class TestChatMemberUpdatedWithoutRequest(TestChatMemberUpdatedBase):
    def test_slot_behaviour(self, chat_member_updated: ChatMemberUpdated[T]) -> None:
        action = chat_member_updated
        for attr in action.__slots__:
            assert getattr(action, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(action)) == len(set(mro_slots(action))), "duplicate slot"

    def test_de_json_required_args(
        self,
        bot: Any,
        user: User,
        chat: Chat,
        old_chat_member: ChatMember,
        new_chat_member: ChatMember,
        time: datetime.datetime,
    ) -> None:
        json_dict: Dict[str, Union[int, bool, str, float]] = {
            "chat": chat.to_dict(),
            "from": user.to_dict(),
            "date": to_timestamp(time),
            "old_chat_member": old_chat_member.to_dict(),
            "new_chat_member": new_chat_member.to_dict(),
        }

        chat_member_updated = ChatMemberUpdated.de_json(json_dict, bot)
        assert chat_member_updated.api_kwargs == {}

        assert chat_member_updated.chat == chat
        assert chat_member_updated.from_user == user
        assert abs(chat_member_updated.date - time) < datetime.timedelta(seconds=1)
        assert to_timestamp(chat_member_updated.date) == to_timestamp(time)
        assert chat_member_updated.old_chat_member == old_chat_member
        assert chat_member_updated.new_chat_member == new_chat_member
        assert chat_member_updated.invite_link is None
        assert chat_member_updated.via_chat_folder_invite_link is None

    def test_de_json_all_args(
        self,
        bot: Any,
        user: User,
        time: datetime.datetime,
        invite_link: ChatInviteLink,
        chat: Chat,
        old_chat_member: ChatMember,
        new_chat_member: ChatMember,
   
