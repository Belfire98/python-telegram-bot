import asyncio
from unittest.mock import patch

import httpx
from http import HTTPStatus
from typing import Any, Callable, Dict, List, Optional

import telegram
from telegram import Bot, Constants, Update
from telegram.bot import Defaults
from telegram.ext import (
    AIORateLimiter,
    Application,
    ApplicationBuilder,
    CallbackDataCache,
    ContextTypes,
    JobQueue,
    PicklePersistence,
    Updater,
)
from telegram.ext._applicationbuilder import _BOT_CHECKS
from telegram.ext._baseupdateprocessor import SimpleUpdateProcessor
from telegram.request import BaseRequest
from telegram.warnings import PTBDeprecationWarning


class TestApplicationBuilderNoOptDeps:
    def test_init(self, builder):
        builder.token("token")
        app = builder.build()
        assert app.job_queue is None


@pytest.mark.skipif(TEST_WITH_OPT_DEPS, reason="Optional dependencies are installed")
class TestApplicationBuilder:
    # ... (rest of the class methods)


# ... (rest of the test classes)
