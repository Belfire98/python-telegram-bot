#!/usr/bin/env python

import pytest
from typing import Tuple, List, Dict, Any
from unittest.mock import Mock

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultAudio,
    InlineQueryResultVoice,
    InputTextMessageContent,
    MessageEntity,
    Bot,
)
from telegram.error import TelegramError
from tests.auxil.slots import mro_slots


@pytest.fixture(scope="module")
def inline_query_result_audio(request) -> InlineQueryResultAudio:
    return InlineQueryResultAudio(
        id_=request.param["id_"],
        audio_url=request.param["audio_url"],
        title=request.param["title"],
        performer=request.param.get("performer"),
        audio_duration=request.param.get("audio_duration"),
        caption=request.param.get("caption"),
        parse_mode=request.param.get("parse_mode"),
        caption_entities=request.param.get("caption_entities", ()),
        input_message_content=request.param.get("input_message_content"),
        reply_markup=request.param.get("reply_markup"),
        bot=request.param.get("bot"),
    )


