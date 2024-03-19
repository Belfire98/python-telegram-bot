import asyncio
import os
from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

import pytest
from telegram import Bot, Document, InputFile, MessageEntity, ParseMode, PhotoSize, ReplyParameters, Voice
from telegram.constants import ParseMode as TelegramParseMode
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
def document_file():
    with data_file("telegram.png").open("rb") as f:
        yield f


@pytest.fixture(scope="module")
async def document(bot, chat_id):
    with data_file("telegram.png").open("rb") as f:
        return (await bot.send_document(chat_id, document=f, read_timeout=50)).document

