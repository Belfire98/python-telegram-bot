#!/usr/bin/env python

import pytest
from copy import deepcopy
from telegram import BotCommandScope, BotCommandScopeType, Dice

def chat_id_fixture(request):
    if request.param == "str":
        return "@supergroupusername"
    return 43

@pytest.fixture(scope="class")
def scope_type_fixture(request):
    return request.param

@pytest.fixture(scope="module")
def scope_class_fixture(request):
    return request.param

@pytest.fixture(scope="module")
def scope_class_and_type_fixture(request):
    return request.param

@pytest.fixture(scope="module")
def bot_command_scope_fixture(scope_class_and_type_fixture, chat_id_fixture):
    class_ = scope_class_and_type_fixture[0]
    type_ = scope_class_and_type_fixture[1]

    if type_ == BotCommandScopeType.CHAT_MEMBER:
        return class_(chat_id=chat_id_fixture, user_id=42)
    return class_(type_, chat_id=chat_id_fixture, user_id=42)

class TestBotCommandScopeWithoutRequest:

    @pytest.mark.parametrize("bot_command_scope", [bot_command_scope_fixture], ids=[BotCommandScope.DEFAULT])
    def test_slot_behaviour(self, bot_command_scope):
        # ... (same as before)

    @pytest.mark.parametrize("scope_class,scope_type", [scope_class_and_type_fixture], ids=[BotCommandScope.DEFAULT])
    def test_de_json(self, scope_class, scope_type, bot, chat_id_fixture):
        # ... (same as before)

    @pytest.mark.parametrize("scope_class,scope_type", [scope_class_and_type_fixture], ids=[BotCommandScope.DEFAULT])
    def test_de_json_invalid_type(self, scope_class, scope_type, bot):
        # ... (same as before)

    @pytest.mark.parametrize("scope_class", [scope_class_fixture], ids=[BotCommandScope.DEFAULT])
    def test_de_json_subclass(self, scope_class, bot, chat_id_fixture):
        # ... (fixed the bug here)

    @pytest.mark.parametrize("bot_command_scope", [bot_command_scope_fixture], ids=[BotCommandScope.DEFAULT])
    def test_to_dict(self, bot_command_scope):
        # ... (same as before)

    @pytest.mark.parametrize("scope", [bot_command_scope_fixture], ids=[BotCommandScope.DEFAULT])
    def test_type_enum_conversion(self, scope):
        # ... (same as before)

    @pytest.mark.parametrize("a,b,c,d,e", [
        (BotCommandScope("base_type"), BotCommandScope("base_type"), bot_command_scope_fixture, deepcopy(bot_command_scope_fixture), Dice(4, "emoji")),
        (BotCommandScope("base_type"), BotCommandScope("base_type"), deepcopy(bot_command_scope_fixture), deepcopy(bot_command_scope_fixture), Dice(4, "emoji")),
    ], ids=["a_vs_b", "a_vs_c", "a_vs_d", "c_vs_d"])
    def test_equality(self, a, b, c, d, e):
        # ... (same as before)
