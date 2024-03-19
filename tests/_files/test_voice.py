import asyncio
import os
from pathlib import Path
from typing import Any
from typing import AsyncContextManager
from typing import AsyncIterator
from typing import Callable
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple
from typing import Union

import pytest
import pytest_asyncio
from _pytest.mark import ParameterSet
from _pytest.mark.structures import ParametrizeInfo
from telegram import Bot
from telegram import InputFile
from telegram import MessageEntity
from telegram import ParseMode
from telegram import ReplyParameters
from telegram.bot import Bot as TelegramBot
from telegram.error import BadRequest
from telegram.error import TelegramError
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
def voice_file() -> AsyncContextManager[bytes]:
    with data_file("telegram.ogg").open("rb") as f:
        yield f.read()


@pytest.fixture(scope="module")
async def voice(bot: TelegramBot, chat_id: int) -> Voice:
    with data_file("telegram.ogg").open("rb") as f:
        return (await bot.send_voice(chat_id, voice=f, read_timeout=50)).voice


class TestVoiceBase:
    duration: int = 3
    mime_type: str = "audio/ogg"
    file_size: int = 9199
    caption: str = "Test *voice*"
    voice_file_url: str = "https://python-telegram-bot.org/static/testfiles/telegram.ogg"
    voice_file_id: str = "5a3128a4d2a04750b5b58397f3b5e812"
    voice_file_unique_id: str = "adc3145fd2e84d95b64d68eaa22aa33e"


class TestVoiceWithoutRequest(TestVoiceBase):
    @pytest.mark.asyncio
    async def test_slot_behaviour(self, voice: Voice) -> None:
        for attr in voice.__slots__:
            assert getattr(voice, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(voice)) == len(set(mro_slots(voice))), "duplicate slot
