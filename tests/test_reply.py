#!/usr/bin/env python

import datetime as dtm
from typing import Any, Dict, Tuple

import pytest
from telegram import (
    BotCommand,
    Chat,
    ExternalReplyInfo,
    Giveaway,
    LinkPreviewOptions,
    MessageEntity,
    MessageOriginUser,
    ReplyParameters,
    TextQuote,
    User,
)
from tests.auxil.slots import mro_slots


@pytest.fixture(scope="module")
def external_reply_info(bot: Any) -> ExternalReplyInfo:
    return ExternalReplyInfo(
        origin=TestExternalReplyInfoBase.origin,
        chat=TestExternalReplyInfoBase.chat,
        message_id=TestExternalReplyInfoBase.message_id,
        link_preview_options=TestExternalReplyInfoBase.link_preview_options,
        giveaway=TestExternalReplyInfoBase.giveaway,
    ).de_json({}, bot)


class TestExternalReplyInfoBase:
    origin = MessageOriginUser(
        dtm.datetime.now(dtm.timezone.utc).replace(microsecond=0), User(1, "user", False)
    )
    chat = Chat(1, Chat.SUPERGROUP)
    message_id = 123
    link_preview_options = LinkPreviewOptions(True)
    giveaway = Giveaway(
        (Chat(1, Chat.CHANNEL), Chat(2, Chat.SUPERGROUP)),
        dtm.datetime.now(dtm.timezone.utc).replace(microsecond=0),
        1,
    )


@pytest.mark.usefixtures("bot")
class TestExternalReplyInfoWithoutRequest(TestExternalReplyInfoBase):
    def test_slot_behaviour(self, external_reply_info: ExternalReplyInfo) -> None:
        for attr in external_reply_info.__slots__:
            assert getattr(external_reply_info, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(external_reply_info)) == len(
            set(mro_slots(external_reply_info))
        ), "duplicate slot"

    def test_de_json(self, bot: Any) -> None:
        json_dict = {
            "origin": self.origin.to_dict(),
            "chat": self.chat.to_dict(),
            "message_id": self.message_id,
            "link_preview_options": self.link_preview_options.to_dict(),
            "giveaway": self.giveaway.to_dict(),
        }

        external_reply_info = ExternalReplyInfo.de_json(json_dict, bot)
        assert external_reply_info.api_kwargs == {}

        assert external_reply_info.origin == self.origin
        assert external_reply_info.chat == self.chat
        assert external_reply_info.message_id == self.message_id
        assert external_reply_info.link_preview_options == self.link_preview_options
        assert external_reply_info.giveaway == self.giveaway

        assert ExternalReplyInfo.de_json(None, bot) is None

    def test_to_dict(self, external_reply_info: ExternalReplyInfo) -> None:
        ext_reply_info_dict = external_reply_info.to_dict()

        assert isinstance(ext_reply_info_dict, dict)
        assert ext_reply_info_dict["origin"] == self.origin.to_dict()
        assert ext_reply_info_dict["chat"] == self.chat.to_dict()
        assert ext_reply_info_dict["message_id"] == self.message_id
        assert ext_reply_info_dict["link_preview_options"] == self.link_preview_options.to_dict()
        assert ext_reply_info_dict["giveaway"] == self.giveaway.to_dict()

    def test_equality(self, external_reply_info: ExternalReplyInfo) -> None:
        a = external_reply_info
        b = ExternalReplyInfo(origin=self.origin)
        c = ExternalReplyInfo(
            origin=MessageOriginUser(dtm.datetime.utcnow(), User(2, "user", False))
        )

        d = BotCommand("start", "description")

        assert a == b
        assert hash(a) == hash(b)

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)


@pytest.fixture(scope="module")
def text_quote(bot: Any) -> TextQuote:
    return TextQuote(
        text=TestTextQuoteBase.text,
        position=TestTextQuoteBase.position,
        entities=TestTextQuoteBase.entities,
        is_manual=TestTextQuoteBase.is_manual,
    ).de_json({}, bot)


class TestTextQuoteBase:
    text = "text"
    position = 1
    entities = [
        MessageEntity(MessageEntity.MENTION, 1, 2),
        MessageEntity(MessageEntity.EMAIL, 3, 4),
    ]
    is_manual = True


@pytest.mark.usefixtures("bot")
class TestTextQuoteWithoutRequest(TestTextQuoteBase):
    def test_slot_behaviour(self, text_quote: TextQuote) -> None:
        for attr in text_quote.__slots__:
            assert getattr(text_quote, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_
