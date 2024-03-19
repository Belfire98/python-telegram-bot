import pytest
from unittest.case import TestCase
from typing import Dict, Any, List, Tuple
from telegram import ChatPermissions, User

class TestChatPermissions(TestCase):
    can_send_messages: bool = True
    can_send_polls: bool = True
    can_send_other_messages: bool = False
    can_add_web_page_previews: bool = False
    can_change_info: bool = False
    can_invite_users: bool = None
    can_pin_messages: bool = None
    can_manage_topics: bool = None
    can_send_audios: bool = True
    can_send_documents: bool = False
    can_send_photos: bool = None
    can_send_videos: bool = True
    can_send_video_notes: bool = False
    can_send_voice_notes: bool = None

    __slots__: Tuple[str, ...] = (
        "can_send_messages",
        "can_send_polls",
        "can_send_other_messages",
        "can_add_web_page_previews",
        "can_change_info",
        "can_invite_users",
        "can_pin_messages",
        "can_manage_topics",
        "can_send_audios",
        "can_send_documents",
        "can_send_photos",
        "can_send_videos",
        "can_send_video_notes",
        "can_send_voice_notes",
    )

    def setUp(self) -> None:
        self.permissions = ChatPermissions(
            can_send_messages=self.can_send_messages,
            can_send_polls=self.can_send_polls,
            can_send_other_messages=self.can_send_other_messages,
            can_add_web_page_previews=self.can_add_web_page_previews,
            can_change_info=self.can_change_info,
            can_invite_users=self.can_invite_users,
            can_pin_messages=self.can_pin_messages,
            can_manage_topics=self.can_manage_topics,
            can_send_audios=self.can_send_audios,
            can_send_documents=self.can_send_documents,
            can_send_photos=self.can_send_photos,
            can_send_videos=self.can_send_videos,
            can_send_video_notes=self.can_send_video_notes,
            can_send_voice_notes=self.can_send_voice_notes,
        )

    def tearDown(self) -> None:
        del self.permissions

    def test_slot_behaviour(self) -> None:
        inst = self.permissions
        for attr in inst.__slots__:
            self.assertEqual(getattr(inst, attr, "err"), f"err", f"got extra slot '{attr}'")
        self.assertEqual(len(vars(inst)), len(set(vars(inst))), "duplicate slot")

    @classmethod
    def de_json(cls, json_dict: Dict[str, Any], bot) -> 'ChatPermissions':
        can_send_media_messages = json_dict.pop("can_send_media_messages", None)
        return ChatPermissions(**json_dict, can_send_media_messages=can_send_media_messages)

    @property
    def api_kwargs(self) -> Dict[str, Any]:
        return {k: getattr(self, k) for k in self.__slots__ if getattr(self, k) is not None}

    def test_de_json(self, bot) -> None:
        json_dict = {
            "can_send_messages": self.can_send_messages,
            "can_send_media_messages": "can_send_media_messages",
            "can_send_polls": self.can_send_polls,
            "can_send_other_messages": self.can_send_other_messages,
            "can_add_web_page_previews": self.can_add_web_page_previews,
            "can_change_info": self.can_change_info,
            "can_invite_users": self.can_invite_users,
            "can_pin_messages": self.can_pin_messages,
            "can_send_audios": self.can_send_audios,
            "can_send_documents": self.can_send_documents,
            "can_send_photos": self.can_send_photos,
            "can_send_videos": self.can_send_videos,
            "can_send_video_notes": self.can_send_video_notes,
            "can_send_voice_notes": self.can_send_voice_notes,
        }
        permissions = self.de_json(json_dict, bot)

