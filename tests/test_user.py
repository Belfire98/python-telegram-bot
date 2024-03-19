#!/usr/bin/env python

import pytest
from unittest.mock import AsyncMock, patch

from telegram import Bot, InlineKeyboardButton, Update, User
from telegram.helpers import escape_markdown
from tests.auxil.bot_method_checks import (
    check_defaults_handling,
    check_shortcut_call,
    check_shortcut_signature,
)
from tests.auxil.slots import mro_slots


@pytest.fixture(scope="module")
def json_dict():
    return {
        "id": TestUserBase.id_,
        "is_bot": TestUserBase.is_bot,
        "first_name": TestUserBase.first_name,
        "last_name": TestUserBase.last_name,
        "username": TestUserBase.username,
        "language_code": TestUserBase.language_code,
        "can_join_groups": TestUserBase.can_join_groups,
        "can_read_all_group_messages": TestUserBase.can_read_all_group_messages,
        "supports_inline_queries": TestUserBase.supports_inline_queries,
        "is_premium": TestUserBase.is_premium,
        "added_to_attachment_menu": TestUserBase.added_to_attachment_menu,
    }


@pytest.fixture()
def user(bot):
    user = User(
        id=TestUserBase.id_,
        first_name=TestUserBase.first_name,
        is_bot=TestUserBase.is_bot,
        last_name=TestUserBase.last_name,
        username=TestUserBase.username,
        language_code=TestUserBase.language_code,
        can_join_groups=TestUserBase.can_join_groups,
        can_read_all_group_messages=TestUserBase.can_read_all_group_messages,
        supports_inline_queries=TestUserBase.supports_inline_queries,
        is_premium=TestUserBase.is_premium,
        added_to_attachment_menu=TestUserBase.added_to_attachment_menu,
    )
    user.set_bot(bot)
    user._unfreeze()
    return user


class TestUserBase:
    id_ = 1
    is_bot = True
    first_name = "first\u2022name"
    last_name = "last\u2022name"
    username = "username"
    language_code = "en_us"
    can_join_groups = True
    can_read_all_group_messages = True
    supports_inline_queries = False
    is_premium = True
    added_to_attachment_menu = False


class TestUserWithoutRequest(TestUserBase):
    def test_slot_behaviour(self, user: User):
        for attr in user.__slots__:
            assert getattr(user, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(user)) == len(set(mro_slots(user))), "duplicate slot"

    def test_de_json(self, json_dict: dict, bot: Bot):
        user = User.de_json(json_dict, bot)
        assert user.api_kwargs == {}

        assert user.id == self.id_
        assert user.is_bot == self.is_bot
        assert user.first_name == self.first_name
        assert user.last_name == self.last_name
        assert user.username == self.username
        assert user.language_code == self.language_code
        assert user.can_join_groups == self.can_join_groups
        assert user.can_read_all_group_messages == self.can_read_all_group_messages
        assert user.supports_inline_queries == self.supports_inline_queries
        assert user.is_premium == self.is_premium
        assert user.added_to_attachment_menu == self.added_to_attachment_menu

    def test_to_dict(self, user: User):
        user_dict = user.to_dict()

        assert isinstance(user_dict, dict)
        assert user_dict["id"] == user.id
        assert user_dict["is_bot"] == user.is_bot
        assert user_dict["first_name"] == user.first_name
        assert user_dict["last_name"] == user.last_name
        assert user_dict["username"] == user.username
        assert user_dict["language_code"] == user.language_code
        assert user_dict["can_join_groups"] == user.can_join_groups
        assert (
            user_dict["can_read_all_group_messages"]
            == user.can_read_all_group_messages
        )
        assert user_dict["supports_inline_queries"] == user.supports_inline_queries
        assert user_dict["is_premium"] == user.is_premium
        assert user_dict["added_to_attachment_menu"] == user.added_to_attachment_menu

    def test_equality(self):
        a = User(self.id_, self.first_name, self.is_bot, self.last_name)
        b = User(self.id_, self.first_name, self.is_bot, self.last_name)
        c = User(self.id_, self.first_name, self.is_bot)
        d = User(0, self.first_name, self.is_bot, self.last_name)
        e = Update(self.id_)

        assert a == b
        assert hash(a) == hash(b)

