#!/usr/bin/env python
import json
import pytest
from typing import Any, Dict, Tuple

import telegram.ext


@pytest.fixture(autouse=True)
def _reset_callback_data_cache(cdc_bot):
    yield
    cdc_bot.callback_data_cache.clear_callback_data()
    cdc_bot.callback_data_cache.clear_callback_queries()


@pytest.fixture()
def bot_data() -> Dict[str, str]:
    return {"test1": "test2", "test3": {"test4": "test5"}}


@pytest.fixture()
def chat_data() -> Dict[int, Dict[str, str]]:
    return {-12345: {"test1": "test2", "test3": {"test4": "test5"}}, -67890: {3: "test4"}}


@pytest.fixture()
def user_data() -> Dict[int, Dict[str, str]]:
    return {12345: {"test1": "test2", "test3": {"test4": "test5"}}, 67890: {3: "test4"}}


@pytest.fixture()
def callback_data() -> Tuple[Tuple[str, int, Dict[str, str]], Dict[str, str]]:
    return (
        (("test1", 1000, {"button1": "test0", "button2": "test1"})),
        {"test1": "test2"},
    )


@pytest.fixture()
def conversations() -> Dict[str, Dict[Tuple[int, int], int]]:
    return {
        "name1": {(123, 123): 3, (456, 654): 4},
        "name2": {(123, 321): 1, (890, 890): 2},
        "name3": {(123, 321): 1, (890, 890): 2},
    }


@pytest.fixture()
def user_data_json(user_data: Dict[int, Dict[str, str]]) -> str:
    return json.dumps(user_data)


@pytest.fixture()
def chat_data_json(chat_data: Dict[int, Dict[str, str]]) -> str:
    return json.dumps(chat_data)


@pytest.fixture()
def bot_data_json(bot_data: Dict[str, str]) -> str:
    return json.dumps(bot_data)


@pytest.fixture()
def callback_data_json(callback_data: Tuple[Tuple[str, int, Dict[str, str]], Dict[str, str]]) -> str:
    return json.dumps(callback_data)


@pytest.fixture()
def conversations_json(conversations: Dict[str, Dict[Tuple[int, int], int]]) -> str:
    return """{"name1": {"[123, 123]": 3, "[456, 654]": 4}, "name2":
              {"[123, 321]": 1, "[890, 890]": 2}, "name3":
              {"[123, 321]": 1, "[890, 890]": 2}}"""


class TestDictPersistence:
    """Just tests the DictPersistence interface. Integration of persistence into Applictation
    is tested in TestBasePersistence!"""

    async def test_slot_behaviour(self):
        inst = telegram.ext.DictPersistence()
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    async def test_no_json_given(self):
        dict_persistence = telegram.ext.DictPersistence()
        assert await dict_persistence.get_user_data() == {}
        assert await dict_persistence.get_chat_data() == {}
        assert await dict_persistence.get_bot_data() == {}
        assert await dict_persistence.get_callback_data() is None
        assert await dict_persistence.get_conversations("noname") == {}

    async def test_bad_json_string_given(self):
        bad_user_data = "thisisnojson99900()))("
        bad_chat_data = "thisisnojson99900()))("
        bad_bot_data = "thisisnojson99900()))("
        bad_callback_data = "thisisnojson99900()))("
        bad_conversations = "thisisnojson99900()))("

        with pytest.raises(TypeError, match="user_data"):
            telegram.ext.DictPersistence(user_data_json=bad_user_data)

        with pytest.raises(TypeError, match="chat_data"):
            telegram.ext.DictPersistence(chat_data_json=bad_chat_data)

        with pytest.raises(TypeError, match="bot_data"):
            telegram.ext.DictPersistence(bot_data_json=bad_bot_data)

        with pytest.raises(TypeError, match="callback_data
