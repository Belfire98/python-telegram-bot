#!/usr/bin/env python

import pytest
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResult,
    InlineQueryResultArticle,
    InlineQueryResultAudio,
    InputTextMessageContent,
)
from telegram.constants import InlineQueryResultType


@pytest.fixture(scope="module")
def inline_query_result_article():
    return InlineQueryResultArticle(
        id_="id",
        title="title",
        input_message_content=InputTextMessageContent("input_message_content"),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("reply_markup")]]),
        url="url",
        hide_url=True,
        description="description",
        thumbnail_url="thumb url",
        thumbnail_height=10,
        thumbnail_width=15,
    )


class TestInlineQueryResultArticleBase:
    id_: str = "id"
    type_: str = "article"
    title: str = "title"
    input_message_content = InputTextMessageContent("input_message_content")
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("reply_markup")]])
    url = "url"
    hide_url = True
    description = "description"
    thumbnail_url = "thumb url"
    thumbnail_height = 10
    thumbnail_width = 15


@pytest.mark.usefixtures("inline_query_result_article")
class TestInlineQueryResultArticleWithoutRequest:
    def test_slot_behaviour(self, inline_query_result_article: InlineQueryResultArticle):
        inst = inline_query_result_article
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(set(mro_slots(inst))) == len(mro_slots(inst)), "duplicate slot"

    def test_expected_values(
        self, inline_query_result_article: InlineQueryResultArticle
    ):
        assert inline_query_result_article.type == TestInlineQueryResultArticleBase.type_
        assert inline_query_result_article.id == TestInlineQueryResultArticleBase.id_
        assert inline_query_result_article.title == TestInlineQueryResultArticleBase.title
        assert (
            inline_query_result_article.input_message_content.to_dict()
            == TestInlineQueryResultArticleBase.input_message_content.to_dict()
        )
        assert inline_query_result_article.reply_markup.to_dict() == TestInlineQueryResultArticleBase.reply_markup.to_dict()
        assert inline_query_result_article.url == TestInlineQueryResultArticleBase.url
        assert inline_query_result_article.hide_url == TestInlineQueryResultArticleBase.hide_url
        assert inline_query_result_article.description == TestInlineQueryResultArticleBase.description
        assert inline_query_result_article.thumbnail_url == TestInlineQueryResultArticleBase.thumbnail_url
        assert inline_query_result_article.thumbnail_height == TestInlineQueryResultArticleBase.thumbnail_height
        assert inline_query_result_article.thumbnail_width == TestInlineQueryResultArticleBase.thumbnail_width

    def test_to_dict(
        self, inline_query_result_article: InlineQueryResultArticle
    ) -> None:
        inline_query_result_article_dict = inline_query_result_article.to_dict()

        assert isinstance(inline_query_result_article_dict, dict)
        assert pytest.assertIsInstance(
            inline_query_result_article_dict["type"], str
        ), f"type should be str, not {type(inline_query_result_article_dict['type'])}"
        assert inline_query_result_article_dict["type"] == inline_query_result_article.type
        assert inline_query_result_article_dict["id"] == inline_query_result_article.id
        assert inline_query_result_article_dict["title"] == inline_query_result_article.title
        assert (
            inline_query_result_article_dict["input_message_content"]
            == inline_query_result_article.input_message_content.to_dict()
        )
        assert (
            inline_query_result_article_dict["reply_markup"]
            == inline_query_result_article.reply_markup.to_dict()
        )
        assert inline_query_result_article_dict["url"] == inline_query_result_article.url
        assert inline_query_result_article_dict["hide_url"] == inline_query_result_article.hide_url
        assert (
            inline_query_result_article_dict["description"]
            == inline_query_result_article.description
        )
        assert (
            inline_query_result_article_dict["thumbnail_url"]
            == inline_query_result_article.thumbnail_url
        )
        assert (
            inline_query_result_article_dict["thumbnail_height"]
            == inline_query_result_article.thumbnail_height
        )
        assert (
            inline_query_result_article_dict["thumbnail_width"]
            == inline_query_result_article.thumbnail_width
        )

    def test_type_enum_conversion(self):
