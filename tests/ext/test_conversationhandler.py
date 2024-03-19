#!/usr/bin/env python
import asyncio
import functools
import logging
import pathlib
import warnings
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pytest
from telegram import (
    CallbackQuery,
    Chat,
    ChosenInlineResult,
    InlineQuery,
    Message,
    MessageEntity,
    PreCheckoutQuery,
    ShippingQuery,
    Update,
    User,
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ApplicationHandlerStop,
    CallbackContext,
    CallbackQueryHandler,
    ChosenInlineResultHandler,
    CommandHandler,
    ConversationHandler,
    Defaults,
    InlineQueryHandler,
    JobQueue,
    MessageHandler,
    PollAnswerHandler,
    PollHandler,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
    StringCommandHandler,
    StringRegexHandler,
    TypeHandler,
    filters,
)
from telegram.warnings import PTBUserWarning
from tests.auxil.build_messages import make_command_message
from tests.auxil.files import PROJECT_ROOT_PATH
from tests.auxil.pytest_classes import PytestBot, make_bot
from tests.auxil.slots import mro_slots


@pytest.fixture(scope="class")
def user1() -> User:
    return User(first_name="Misses Test", id=123, is_bot=False)


@pytest.fixture(scope="class")
def user2() -> User:
    return User(first_name="Mister Test", id=124, is_bot=False)


def raise_ahs(func: Callable) -> Callable:
    @functools.wraps(func)  # for checking __repr__
    async def decorator(self: Any, *args: Any, **kwargs: Any) -> Any:
        result = await func(self, *args, **kwargs)
        if self.raise_app_handler_stop:
            raise ApplicationHandlerStop(result)
        return result

    return decorator


class TestConversationHandler:
    """Persistence of conversations is tested in test_basepersistence.py"""

    # State definitions
    # At first we're thirsty.  Then we brew coffee, we drink it
    # and then we can start coding!
    END, THIRSTY, BREWING, DRINKING, CODING = range(-1, 4)

    # Drinking state definitions (nested)
    # At first we're holding the cup.  Then we sip coffee, and last we swallow it
    HOLDING, SIPPING, SWALLOWING, REPLENISHING, STOPPING = map(chr, range(ord("a"), ord("f")))

    current_state: Dict[int, int]
    entry_points: List[Union[CommandHandler, CallbackQueryHandler]]
    states: Dict[int, List[Union[CommandHandler, CallbackQueryHandler]]]
    fallbacks: List[Union[CommandHandler, CallbackQueryHandler]]
    group: Chat
    second_group: Chat

    raise_app_handler_stop: bool
    test_flag: bool

    # Test related
    @pytest.fixture(autouse=True)
    def _reset(self) -> None:
        self.raise_app_handler_stop = False
        self.test_flag = False
        self.current_state = {}
        self.entry_points = [CommandHandler("start", self.start)]
        self.states = {
            self.THIRSTY: [CommandHandler("brew", self.brew), CommandHandler("wait", self.start)],
            self.BREWING: [CommandHandler("pourCoffee", self.drink)],
            self.DRINKING: [
                CommandHandler("startCoding", self.code),
                CommandHandler("drinkMore", self.drink),
                CommandHandler("end", self.end),
            ],
            self.CODING: [
                CommandHandler("keepCoding", self.code),
                CommandHandler("gettingThirsty", self.start),
                CommandHandler("drinkMore", self.drink),
            ],
        }
        self.fallbacks = [CommandHandler("eat", self.start)]
        self.is_timeout = False

        # for nesting tests
        self.nested_states = {
            self.THIRSTY: [CommandHandler("brew", self.brew), CommandHandler("wait", self.start)],
            self.BREWING: [CommandHandler("pourCoffee", self.drink)],
            self.CODING: [
                CommandHandler("keepCoding", self.code),
                CommandHandler("gettingThirsty", self.start),
                CommandHandler("drinkMore", self.drink),
            ],
        }
        self.drinking_entry_points = [CommandHandler("hold", self.hold)]
        self.drinking_states = {
            self.HOLDING: [CommandHandler("sip", self.sip)],
            self.SIPPING: [CommandHandler("swallow", self.swallow)],
            self.SWALLOWING: [CommandHandler("hold", self.hold)],
        }
        self.drinking_fallbacks = [
            CommandHandler("replenish", self.replenish),
            CommandHandler("stop", self.stop),
            CommandHandler("end", self.end),
            CommandHandler("startCoding", self.code),
            Command
