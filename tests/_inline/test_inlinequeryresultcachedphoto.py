#!/usr/bin/env python

import pytest
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedVoice,
    InputTextMessageContent,
    MessageEntity,
)
from tests.auxil.slots import mro_slots


class TestInlineQueryResultCachedPhoto:
    """Tests for InlineQueryResultCachedPhoto class."""

    id_ = "id"
    type_ = "photo"
    photo_file_id = "photo file id"
    title = "title"
    description = "description"
    caption = "caption"
    parse_mode = "HTML"
    caption_entities = [MessageEntity(MessageEntity.ITALIC, 0, 7)]
    input_message_content = InputTextMessageContent("input_message_content")
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("reply_markup")]])

    @pytest.fixture(scope="module")
    def inline_query_result_cached_photo(self):
        return InlineQueryResultCachedPhoto(
            self.id_,
            self.photo_file_id,
            title=self.title,
            description=self.description,
            caption=self.caption,
            parse_mode=self.parse_mode,
            caption_entities=self.caption_entities,
            input_message_content=self.input_message_content,
            reply_markup=self.reply_markup,
        )

    def test_slot_behaviour(self, inline_query_result_cached_photo):
        inst = inline_query_result_cached_photo
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    @pytest.mark.parametrize(
        "attributes,expected_values",
        [
            (
                ["type", "id", "photo_file_id", "title", "description"],
                {
                    "type": type_.type_,
                    "id": id_,
                    "photo_file_id": photo_file_id,
                    "title": title,
                    "description": description,
                },
            ),
            (
                ["caption", "parse_mode", "caption_entities"],
                {
                    "caption": caption,
                    "parse_mode": parse_mode,
                    "caption_entities": tuple(caption_entities),
                },
            ),
            (
                ["input_message_content"],
                {
                    "input_message_content": input_message_content.to_dict(),
                },
            ),
            (
                ["reply_markup"],
                {
                    "reply_markup": reply_markup.to_dict(),
                },
            ),
        ],
    )
    def test_expected_values(
        self, inline_query_result_cached_photo, attributes, expected_values
    ):
        for attr in attributes:
            assert getattr(inline_query_result_cached_photo, attr) == expected_values[attr]

    def test_caption_entities_always_tuple(self, inline_query_result_cached_photo):
        result = InlineQueryResultCachedPhoto(self.id_, self.photo_file_id)
        assert result.caption_entities == ()

    def test_to_dict(self, inline_query_result_cached_photo):
        inline_query_result_cached_photo_dict = inline_query_result_cached_photo.to_dict()

        assert isinstance(inline_query_result_cached_photo_dict, dict)
        for key, value in inline_query_result_cached_photo_dict.items():
            if key == "caption_entities":
                assert all(isinstance(ce, dict) for ce in value)
            else:
                assert value == getattr(inline_query_result_cached_photo, key)

    def test_equality(self):
        a = InlineQueryResultCachedPhoto(self.id_, self.photo_file_id)
        b = InlineQueryResultCachedPhoto(self.id_, self.photo_file_id)
        c = InlineQueryResultCachedPhoto(self.id_, "")
        d = InlineQueryResultCachedPhoto("", self.photo_file_id)
        e = InlineQueryResultCachedVoice(self.id_, "", "")

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a == c
        assert hash(a) == hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
