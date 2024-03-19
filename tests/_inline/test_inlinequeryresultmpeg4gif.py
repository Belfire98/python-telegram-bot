#!/usr/bin/env python

import pytest
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultMpeg4Gif,
    InlineQueryResultVoice,
    InputTextMessageContent,
    MessageEntity,
)
from tests.auxil.slots import mro_slots

class TestInlineQueryResultMpeg4GifBase:
    id_: str = "id"
    type_: str = "mpeg4_gif"
    mpeg4_url: str = "mpeg4 url"
    mpeg4_width: int = 10
    mpeg4_height: int = 15
    mpeg4_duration: int = 1
    thumbnail_url: str = "thumb url"
    thumbnail_mime_type: str = "image/jpeg"
    title: str = "title"
    caption: str = "caption"
    parse_mode: str = "Markdown"
    caption_entities: tuple[MessageEntity] = tuple([MessageEntity(MessageEntity.ITALIC, 0, 7)])
    input_message_content: InputTextMessageContent = InputTextMessageContent("input_message_content")
    reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup([[InlineKeyboardButton("reply_markup")]])

class TestInlineQueryResultMpeg4Gif(TestInlineQueryResultMpeg4GifBase):
    @pytest.fixture(scope="module")
    def inline_query_result_mpeg4_gif(self):
        return InlineQueryResultMpeg4Gif(
            self.id_,
            self.mpeg4_url,
            self.thumbnail_url,
            mpeg4_width=self.mpeg4_width,
            mpeg4_height=self.mpeg4_height,
            mpeg4_duration=self.mpeg4_duration,
            title=self.title,
            caption=self.caption,
            parse_mode=self.parse_mode,
            caption_entities=self.caption_entities,
            input_message_content=self.input_message_content,
            reply_markup=self.reply_markup,
            thumbnail_mime_type=self.thumbnail_mime_type,
        )

    def test_slot_behaviour(self, inline_query_result_mpeg4_gif: InlineQueryResultMpeg4Gif):
        inst = inline_query_result_mpeg4_gif
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    def test_expected_values(self, inline_query_result_mpeg4_gif: InlineQueryResultMpeg4Gif):
        assert inline_query_result_mpeg4_gif.type == self.type_
        assert inline_query_result_mpeg4_gif.id == self.id_
        assert inline_query_result_mpeg4_gif.mpeg4_url == self.mpeg4_url
        assert inline_query_result_mpeg4_gif.mpeg4_width == self.mpeg4_width
        assert inline_query_result_mpeg4_gif.mpeg4_height == self.mpeg4_height
        assert inline_query_result_mpeg4_gif.mpeg4_duration == self.mpeg4_duration
        assert inline_query_result_mpeg4_gif.thumbnail_url == self.thumbnail_url
        assert inline_query_result_mpeg4_gif.thumbnail_mime_type == self.thumbnail_mime_type
        assert inline_query_result_mpeg4_gif.title == self.title
        assert inline_query_result_mpeg4_gif.caption == self.caption
        assert inline_query_result_mpeg4_gif.parse_mode == self.parse_mode
        assert inline_query_result_mpeg4_gif.caption_entities == self.caption_entities
        assert (
            inline_query_result_mpeg4_gif.input_message_content.to_dict()
            == self.input_message_content.to_dict()
        )
        assert inline_query_result_mpeg4_gif.reply_markup.to_dict() == self.reply_markup.to_dict()

    def test_caption_entities_always_tuple(self):
        result = InlineQueryResultMpeg4Gif(self.id_, self.mpeg4_url, self.thumbnail_url)
        assert result.caption_entities == ()

    def test_to_dict(self, inline_query_result_mpeg4_gif: InlineQueryResultMpeg4Gif):
        inline_query_result_mpeg4_gif_dict = inline_query_result_mpeg4_gif.to_dict()

        assert isinstance(inline_query_result_mpeg4_gif_dict, dict)
        assert inline_query_result_mpeg4_gif_dict["type"] == inline_query_result_mpeg4_gif.type
        assert inline_query_result_mpeg4_gif_dict["id"] == inline_query_result_mpeg4_gif.id
        assert (
            inline_query_result_mpeg4_gif_dict["mpeg4_url"]
            == inline_query_result_mpeg4_gif.mpeg4_url
        )
        assert (
           
