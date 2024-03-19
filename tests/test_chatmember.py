#!/usr/bin/env python

import datetime
import inspect
from copy import deepcopy
from typing import Any

import pytest
from telegram import (
    ChatMember,
    ChatMemberAdministrator,
    ChatMemberBanned,
    ChatMemberLeft,
    ChatMemberMember,
    ChatMemberOwner,
    ChatMemberRestricted,
    Dice,
    User,
)
from telegram._utils.datetime import UTC, to_timestamp
from tests.auxil.slots import mro_slots
from telegram.chatmember import ChatMemberStatus

ignored = ["self", "api_kwargs"]


class CMDefaults:
    user = User(1, "First name", False)
    custom_title: str = "PTB"
    is_anonymous: bool = True
    until_date: datetime.datetime = to_timestamp(datetime.datetime.utcnow())
    can_be_edited: bool = False
    can_change_info: bool = True
    can_post_messages: bool = True
    can_edit_messages: bool = True
    can_delete_messages: bool = True
    can_invite_users: bool = True
    can_restrict_members: bool = True
    can_pin_messages: bool = True
    can_promote_members: bool = True
    can_send_messages: bool = True
    can_send_media_messages: bool = True
    can_send_polls: bool = True
    can_send_other_messages: bool = True
    can_add_web_page_previews: bool = True
    is_member: bool = True
    can_manage_chat: bool = True
    can_manage_video_chats: bool = True
    can_manage_topics: bool = True
    can_send_audios: bool = True
    can_send_documents: bool = True
    can_send_photos: bool = True
    can_send_videos: bool = True
    can_send_video_notes: bool = True
    can_send_voice_notes: bool = True
    can_post_stories: bool = True
    can_edit_stories: bool = True
    can_delete_stories: bool = True


def chat_member_owner() -> ChatMemberOwner:
    return ChatMemberOwner(CMDefaults.user, CMDefaults.is_anonymous, CMDefaults.custom_title)


def chat_member_administrator() -> ChatMemberAdministrator:
    return ChatMemberAdministrator(
        CMDefaults.user,
        CMDefaults.can_be_edited,
        CMDefaults.is_anonymous,
        CMDefaults.can_manage_chat,
        CMDefaults.can_delete_messages,
        CMDefaults.can_manage_video_chats,
        CMDefaults.can_restrict_members,
        CMDefaults.can_promote_members,
        CMDefaults.can_change_info,
        CMDefaults.can_invite_users,
        CMDefaults.can_post_messages,
        CMDefaults.can_edit_messages,
        CMDefaults.can_pin_messages,
        CMDefaults.can_manage_topics,
        CMDefaults.custom_title,
        CMDefaults.can_post_stories,
        CMDefaults.can_edit_stories,
        CMDefaults.can_delete_stories,
    )


def chat_member_member() -> ChatMemberMember:
    return ChatMemberMember(CMDefaults.user)


def chat_member_restricted() -> ChatMemberRestricted:
    return ChatMemberRestricted(
        CMDefaults.user,
        CMDefaults.is_member,
        CMDefaults.can_change_info,
        CMDefaults.can_invite_users,
        CMDefaults.can_pin_messages,
        CMDefaults.can_send_messages,
        CMDefaults.can_send_polls,
        CMDefaults.can_send_other_messages,
        CMDefaults.can_add_web_page_previews,
        CMDefaults.can_manage_topics,
        CMDefaults.until_date,
        CMDefaults.can_send_audios,
        CMDefaults.can_send_documents,
        CMDefaults.can_send_photos,
        CMDefaults.can_send_videos,
        CMDefaults.can_send_video_notes,
        CMDefaults.can_send_voice_notes,
    )


def chat_member_left() -> ChatMemberLeft:
