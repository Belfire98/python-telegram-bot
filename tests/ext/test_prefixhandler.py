import pytest
from typing import List, Tuple, Union, Any, Dict, Callable, Optional, Iterable
from unittest.mock import Mock

import telegram
from telegram.ext import CallbackContext, PrefixHandler, filters
from tests.auxil.build_messages import make_command_update, make_message, make_message_update
from tests.auxil.slots import mro_slots
from tests.ext.test_commandhandler import BaseTest, is_match

class TestPrefixHandlerSlotBehavior(BaseTest):
    def test_slot_behaviour(self):
        handler = self.make_default_handler()
        for attr in handler.__slots__:
            assert getattr(handler, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(handler)) == len(set(mro_slots(handler))), "duplicate slot"

class TestPrefixHandlerBasic(BaseTest):
    PREFIXES = ["!", "#", "mytrig-"]
    COMMANDS = ["help", "test"]

    @pytest.fixture(scope="class", params=PREFIXES)
    def prefix(self, request):
        return request.param

    @pytest.fixture(scope="class", params=[1, 2], ids=["single prefix", "multiple prefixes"])
    def prefixes(self, request):
        return TestPrefixHandler.PREFIXES[: request.param]

    @pytest.fixture(scope="class", params=COMMANDS)
    def command(self, request):
        return request.param

    @pytest.fixture(scope="class", params=[1, 2], ids=["single command", "multiple commands"])
    def commands(self, request):
        return TestPrefixHandler.COMMANDS[: request.param]

    @pytest.fixture(scope="class")
    def prefix_message_text(self, prefix, command):
        return prefix + command

    @pytest.fixture(scope="class")
    def prefix_message(self, prefix_message_text):
        return make_message(prefix_message_text)

    @pytest.fixture(scope="class")
    def prefix_message_update(self, prefix_message):
        return make_message_update(prefix_message)

    def make_default_handler(self, callback: Callable[[telegram.Message], bool] = None, **kwargs) -> PrefixHandler:
        callback = callback or self.callback_basic
        return PrefixHandler(self.PREFIXES, self.COMMANDS, callback, **kwargs)

    def test_basic(
        self,
        app: Any,
        prefix: str,
        command: str,
    ):
        """Test the basic expected response from a prefix handler"""
        handler = self.make_default_handler()
        app.add_handler(handler)
        text = prefix + command

        assert self.response(app, make_message_update(text))
        assert not is_match(handler, make_message_update(command))
        assert not is_match(handler, make_message_update(prefix + "notacommand"))
        assert not is_match(handler, make_command_update(f"not {text} at start"))
        assert not is_match(
            handler, make_message_update(bot=app.bot, message=None, caption="caption")
        )

class TestPrefixHandlerCombinations(BaseTest):
    PREFIXES = ["!", "#", "mytrig-"]
    COMMANDS = ["help", "test"]

    @pytest.fixture(scope="class", params=PREFIXES)
    def prefix(self, request):
        return request.param

    @pytest.fixture(scope="class", params=[1, 2], ids=["single prefix", "multiple prefixes"])
    def prefixes(self, request):
        return TestPrefixHandler.PREFIXES[: request.param]

    @pytest.fixture(scope="class", params=COMMANDS)
    def command(self, request):
        return request.param

    @pytest.fixture(scope="class", params=[1, 2], ids=["single command", "multiple commands"])
    def commands(self, request):
        return TestPrefixHandler.COMMANDS[: request.param]

    @pytest.fixture(scope="class")
    def prefix_message_update(self, prefix: str, command: str):
        prefix_message_text = prefix + command
        prefix_message = make_message(prefix_message_text)
        return make_message_update(prefix_message)

    def test_single_multi_prefixes_commands(
        self,
        prefixes: Tuple[str, ...],
        commands: Tuple[str, ...],
        prefix_message_update: telegram.Update,
    ):
        """Test various combinations of prefixes and commands"""
        handler = self.make_default_handler()
        result = is_match(handler, prefix_message_update)
        expected = prefix_message_update.message.text in combinations(prefixes, commands)
        assert result == expected

class TestPrefixHandlerEdited(BaseTest):
    PREFIXES = ["!", "#", "mytrig-"]
    COMMANDS = ["help", "test"]

    @pytest.fixture(scope="class", params=PREFIXES)
    def prefix(self, request):
        return request.param

    @pytest.fixture(scope="class", params=[1, 2], ids=["single prefix", "multiple prefixes"])
    def prefixes(self, request):
        return TestPrefixHandler.PREFIXES[: request.param]

    @pytest.fixture(scope="class",
