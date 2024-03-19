import asyncio
from unittest.mock import AsyncMock, patch

import pytest
from telegram import (
    Bot,
    Chat,
    ChatLocation,
    ChatPermissions,
    Location,
    ReactionTypeCustomEmoji,
    ReactionTypeEmoji,
    User,
)
from telegram._utils.datetime import UTC, to_timestamp
from telegram.constants import ChatAction, ChatType, ReactionEmoji
from telegram.helpers import escape_markdown


@pytest.fixture
def chat(bot):
    """A chat fixture to use in the test methods."""
    chat = Chat(
        TestChatBase.id_,
        title=TestChatBase.title,
        type_=TestChatBase.type_,
        username=TestChatBase.username,
        sticker_set_name=TestChatBase.sticker_set_name,
        can_set_sticker_set=TestChatBase.can_set_sticker_set,
        permissions=TestChatBase.permissions,
        slow_mode_delay=TestChatBase.slow_mode_delay,
        bio=TestChatBase.bio,
        linked_chat_id=TestChatBase.linked_chat_id,
        location=TestChatBase.location,
        has_private_forwards=True,
        has_protected_content=True,
        has_visible_history=True,
        join_to_send_messages=True,
        join_by_request=True,
        has_restricted_voice_and_video_messages=True,
        is_forum=True,
        active_usernames=TestChatBase.active_usernames,
        emoji_status_custom_emoji_id=TestChatBase.emoji_status_custom_emoji_id,
        emoji_status_expiration_date=TestChatBase.emoji_status_expiration_date,
        has_aggressive_anti_spam_enabled=TestChatBase.has_aggressive_anti_spam_enabled,
        has_hidden_members=TestChatBase.has_hidden_members,
        available_reactions=TestChatBase.available_reactions,
        accent_color_id=TestChatBase.accent_color_id,
        background_custom_emoji_id=TestChatBase.background_custom_emoji_id,
        profile_accent_color_id=TestChatBase.profile_accent_color_id,
        profile_background_custom_emoji_id=TestChatBase.profile_background_custom_emoji_id,
        unrestrict_boost_count=TestChatBase.unrestrict_boost_count,
        custom_emoji_sticker_set_name=TestChatBase.custom_emoji_sticker_set_name,
    )
    chat.set_bot(bot)
    chat._unfreeze()
    return chat


class TestChatBase:
    id_ = -28767330
    title = "ToledosPalaceBot - Group"
    type_ = "group"
    username = "username"
    all_members_are_administrators = False
    sticker_set_name = "stickers"
    can_set_sticker_set = False
    permissions = ChatPermissions(
        can_send_messages=True,
        can_change_info=False,
        can_invite_users=True,
    )
    slow_mode_delay = 30
    bio = "I'm a Barbie Girl in a Barbie World"
    linked_chat_id = 11880
    location = ChatLocation(Location(123, 456), "Barbie World")
    has_protected_content = True
    has_visible_history = True
    has_private_forwards = True
    join_to_send_messages = True
    join_by_request = True
    has_restricted_voice_and_video_messages = True
    is_forum = True
    active_usernames = ["These", "Are", "Usernames!"]
    emoji_status_custom_emoji_id = "VeryUniqueCustomEmojiID"
    emoji_status_expiration_date = datetime.datetime.now(tz=UTC).replace(microsecond=0)
    has_aggressive_anti_spam_enabled = True
    has_hidden_members = True
    available_reactions = [
        ReactionTypeEmoji(ReactionEmoji.THUMBS_DOWN),
        ReactionTypeCustomEmoji("custom_emoji_id"),
    ]
    accent_color_id = 1
    background_custom_emoji_id = "background_custom_emoji_id"
    profile_accent_color_id = 2
    profile_background_custom_emoji_id = "profile_background_
