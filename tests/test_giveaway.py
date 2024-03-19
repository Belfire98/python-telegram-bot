#!/usr/bin/env python

"""A library that provides a Python interface to the Telegram Bot API"""

import datetime as dtm
import pytest
from typing import Any, Dict, Tuple

import telegram
from telegram._utils.datetime import to_timestamp
from telegram.error import TelegramError
from tests.auxil.slots import mro_slots

