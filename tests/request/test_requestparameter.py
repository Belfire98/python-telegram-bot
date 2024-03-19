#!/usr/bin/env python

import datetime
import pytest
from typing import Any
from typing import List
from typing import Optional
from typing import Sequence

import telegram
from telegram import InputFile
from telegram import InputMediaPhoto
from telegram import InputMediaVideo
from telegram import InputSticker
from telegram.constants import ChatType
from telegram.request._requestparameter import RequestParameter
from tests.auxil.files import data_file


class TestRequestParameterWithoutRequest:
    @pytest.fixture
    def request_parameter(self, value: Any, input_files: Optional[List[InputFile]] = None) -> RequestParameter:
        return RequestParameter("name", value, input_files)

    def test_slot_behaviour(self, request_parameter: RequestParameter) -> None:
        for attr in request_parameter.__slots__:
            assert getattr(request_parameter, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len({slot for slot in mro_slots(request_parameter)}) == len(request_parameter.__slots__), "duplicate slot"

    def test_init(self, request_parameter: RequestParameter) -> None:
        assert request_parameter.name == "name"
        assert request_parameter.value == "value"
        assert request_parameter.input_files == [1, 2] if request_parameter.input_files else None

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (1, "1"),
            ("one", "one"),
            (True, "true"),
            (None, None),
            ([1, "1"], '[1, "1"]'),
            ({True: None}, '{"true": null}'),
            ((1,), "[1]"),
        ],
    )
    def test_json_value(self, value: Any, expected: str, request_parameter: RequestParameter) -> None:
        request_parameter.value = value
        assert request_parameter.json_value == expected

    @pytest.mark.parametrize(
        ("value", "expected_value"),
        [
            (True, True),
            ("str", "str"),
            ({1: 1.0}, {1: 1.0}),
            (ChatType.PRIVATE, "private"),
            (telegram.MessageEntity("type", 1, 1), {"type": "type", "offset": 1, "length": 1}),
            (datetime.datetime(2019, 11, 11, 0, 26, 16, 10**5), 1573431976),
            (
                [
                    True,
                    "str",
                    telegram.MessageEntity("type", 1, 1),
                    ChatType.PRIVATE,
                    datetime.datetime(2019, 11, 11, 0, 26, 16, 10**5),
                ],
                [True, "str", {"type": "type", "offset": 1, "length": 1}, "private", 1573431976],
            ),
        ],
    )
    def test_from_input_no_media(
        self, value: Any, expected_value: Any, request_parameter: RequestParameter
    ) -> None:
        request_parameter.value = value
        request_parameter.input_files = None
        result = RequestParameter.from_input("key", request_parameter)
        assert result.value == expected_value
        assert result.input_files is None

    def test_from_input_inputfile(self) -> None:
        input_file_1 = InputFile("data1", filename="inputfile_1", attach=True)
        input_file_2 = InputFile("data2", filename="inputfile_2")

        request_parameter = RequestParameter.from_input("key", input_file_1)
        assert request_parameter.value == input_file_1.attach_uri
        assert request_parameter.input_files == [input_file_1]

        request_parameter = RequestParameter.from_input("key", input_file_2)
        assert request_parameter.value is None
        assert request_parameter.input_files == [input_file_2]

        request_parameter = RequestParameter.from_input("key", [input_file_1, input_file_2])
        assert request_parameter.value == [input_file_1.attach_uri]
        assert request_parameter.input_files == [input_file_1, input_file_2]

    @pytest.mark.parametrize(
        ("value", "expected_value"),
        [
            (telegram.InputMediaPhoto(media=data_file("telegram.jpg").read_bytes()), {"type": "photo"}),
            (
                telegram.InputMediaVideo(
                    media=data_file("telegram.mp4").read_bytes(),
                    thumbnail=data_file("telegram.jpg").read_bytes(),
                ),
                {"type": "video", "thumb": "attach://telegram.jpg"},
            ),
        ],
    )
    def test_from_input_input_media(
        self, value: telegram.InputMediaBase, expected_value: dict, request_parameter: RequestParameter
    ) -> None:
        request_parameter.value = value
        result = RequestParameter.from_input("key", request_parameter)
        assert result.value == expected_value
        assert result.input_files == [value.
