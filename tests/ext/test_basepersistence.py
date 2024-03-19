#!/usr/bin/env python

import asyncio
import collections
import copy
import enum
import functools
import logging
import sys
import time
from pathlib import Path
from typing import NamedTuple, Optional

import pytest
from telegram import Bot, Chat, InlineKeyboardButton, InlineKeyboardMarkup, Update, User
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ApplicationHandlerStop,
    BaseHandler,
    BasePersistence,
    CallbackContext,
    ConversationHandler,
    ExtBot,
    MessageHandler,
    PersistenceInput,
    filters,
)
from telegram.warnings import PTBUserWarning
from tests.auxil.build_messages import make_message_update
from tests.auxil.pytest_classes import PytestApplication, make_bot
from tests.auxil.slots import mro_slots


