#!/usr/bin/env python

"""Tests for the Video class."""

import asyncio
import os
from pathlib import Path
from typing import Any

import pytest
from pytest import mark
from telegram import Bot, InputFile, MessageEntity, PhotoSize, ReplyParameters, Video, Voice
from telegram.constants import ParseMode
from telegram.error import BadRequest, TelegramError
from telegram.helpers import escape_markdown
from telegram.request import RequestData
from tests.auxil.bot_method_checks import (
    check_defaults_handling,
    check_shortcut_call,
    check_shortcut_signature,
)
from tests.auxil.build_messages import make_message
from tests.auxil.files import data_file
from tests.auxil.slots import mro_slots


@pytest.fixture()
def video_file():
    with data_file("telegram.mp4").open("rb") as f:
        yield f


@pytest.fixture(scope="module")
async def video(bot: Bot, chat_id: int):
    with data_file("telegram.mp4").open("rb") as f:
        return (await bot.send_video(chat_id, video=f, read_timeout=50)).video


class TestVideo:
    """Tests for the Video class."""

    width: int = 360
    height: int = 640
    duration: int = 5
    file_size: int = 326534
    mime_type: str = "video/mp4"
    supports_streaming: bool = True
    file_name: str = "telegram.mp4"
    thumb_width: int = 180
    thumb_height: int = 320
    thumb_file_size: int = 1767
    caption: str = "<b>VideoTest</b> - *Caption*"
    video_file_url: str = "https://python-telegram-bot.org/static/testfiles/telegram.mp4"
    video_file_id: str = "5a3128a4d2a04750b5b58397f3b5e812"
    video_file_unique_id: str = "adc3145fd2e84d95b64d68eaa22aa33e"

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, video):
        """Setup and teardown for each test method."""
        self.video = video

    @mark.asyncio
    async def test_slot_behaviour(self, video):
        """Test slot behaviour."""
        for attr in video.__slots__:
            assert getattr(video, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(video)) == len(set(mro_slots(video))), "duplicate slot"

    @mark.asyncio
    async def test_creation(self, video):
        """Test creation."""
        # Make sure file has been uploaded.
        assert isinstance(video, Video)
        assert isinstance(video.file_id, str)
        assert isinstance(video.file_unique_id, str)
        assert video.file_id
        assert video.file_unique_id

        assert isinstance(video.thumbnail, PhotoSize)
        assert isinstance(video.thumbnail.file_id, str)
        assert isinstance(video.thumbnail.file_unique_id, str)
        assert video.thumbnail.file_id
        assert video.thumbnail.file_unique_id

