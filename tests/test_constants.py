#!/usr/bin/env python

import asyncio
import json
from typing import Any
from typing import Tuple

import telegram
from telegram import Message
from telegram._utils.enum import IntEnum
from telegram._utils.enum import StringEnum
from telegram.error import BadRequest
from tests.auxil.build_messages import make_message
from tests.auxil.files import data_file
from tests.auxil.string_manipulation import to_snake_case


class StrEnumTest(StringEnum):
    FOO = "foo"
    BAR = "bar"


class IntEnumTest(IntEnum):
    FOO = 1
    BAR = 2


class TestConstantsWithoutRequest:
    """Test the completeness and consistency of the constants in the telegram.constants module."""

    def test__all__(self):
        """Test if all constants are listed in constants.__all__."""
        expected = {
            key
            for key, member in telegram.constants.__dict__.items()
            if (
                not key.startswith("_")
                # exclude imported stuff
                and getattr(member, "__module__", "telegram.constants") == "telegram.constants"
                and key not in ("sys", "datetime")
            )
        }
        actual = set(telegram.constants.__all__)
        assert actual == expected

    def test_message_attachment_type(self):
        """Test if all MessageAttachmentType members are in MessageType."""
        assert all(
            getattr(telegram.constants.MessageType, x.name, False)
            for x in telegram.constants.MessageAttachmentType
        )

    def test_to_json(self):
        """Test if StringEnum and IntEnum members can be serialized to JSON."""
        assert json.dumps(StrEnumTest.FOO) == json.dumps("foo")
        assert json.dumps(IntEnumTest.FOO) == json.dumps(1)

    def test_string_representation(self):
        """Test the string representation of StringEnum members."""
        # test __repr__
        assert repr(StrEnumTest.FOO) == "<StrEnumTest.FOO>"

        # test __format__
        assert f"{StrEnumTest.FOO} this {StrEnumTest.BAR}" == "foo this bar"
        assert f"{StrEnumTest.FOO:*^10}" == "***foo****"

        # test __str__
        assert str(StrEnumTest.FOO) == "foo"

    def test_int_representation(self):
        """Test the int representation of IntEnum members."""
        # test __repr__
        assert repr(IntEnumTest.FOO) == "<IntEnumTest.FOO>"

        # test __format__
        assert f"{IntEnumTest.FOO}/0 is undefined!" == "1/0 is undefined!"
        assert f"{IntEnumTest.FOO:*^10}" == "****1*****"

        # test __str__
        assert str(IntEnumTest.FOO) == "1"

    def test_string_inheritance(self):
        """Test the inheritance of StringEnum members."""
        assert isinstance(StrEnumTest.FOO, str)
        assert StrEnumTest.FOO + StrEnumTest.BAR == "foobar"
        assert StrEnumTest.FOO.replace("o", "a") == "faa"

