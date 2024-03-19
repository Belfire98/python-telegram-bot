#!/usr/bin/env python

import asyncio
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Optional, Type, Union

import pytest

import telegram
from telegram.ext import CallbackContext, JobQueue, TypeHandler
from tests.auxil.slots import mro_slots


class TestTypeHandler:
    test_flag: bool = False

    @pytest.fixture(autouse=True)
    def _reset(self):
        self.test_flag = False

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ("check_update", Callable[[Dict[str, Any]], bool]),
            ("process_update", Callable[[Dict[str, Any]], None]),
            ("__init__", Callable[[Type[Dict[str, Any]], Callable], None]),
        ],
    )
    def test_slot_behaviour(self, attr: str, expected: Type[Callable]):
        inst = TypeHandler(dict, self.callback)
        for slot in mro_slots(inst):
            attr_value = getattr(inst, slot, "err")
            if slot == attr:
                assert isinstance(attr_value, expected), f"got wrong type for slot '{slot}'"
            elif attr_value != "err":
                assert not isinstance(attr_value, expected), f"got extra slot '{slot}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    @pytest.mark.parametrize(
        "update,expected",
        [
            ({"a": 1, "b": 2}, True),
            ("not a dict", False),
        ],
    )
    async def test_check_update(self, update: Union[Dict[str, Any], str], expected: bool):
        handler = TypeHandler(dict, self.callback)
        assert handler.check_update(update) == expected

    @pytest.mark.parametrize(
        "update,expected",
        [
            ({"a": 1, "b": 2}, None),
        ],
    )
    async def test_process_update(self, app, update: Dict[str, Any], expected: Optional[None]):
        handler = TypeHandler(dict, self.callback)
        app.add_handler(handler)
        await app.process_update(update)
        assert self.test_flag == expected

    @pytest.mark.parametrize(
        "update,strict,expected",
        [
            ({"a": 1, "b": 2}, False, True),
            (OrderedDict({"a": 1, "b": 2}), False, True),
            ({"a": 1, "b": 2}, True, True),
            (OrderedDict({"a": 1, "b": 2}), True
