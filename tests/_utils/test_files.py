#!/usr/bin/env python

import contextlib
import subprocess
import sys
from pathlib import Path
from typing import Any, BinaryIO, InputFile, Union

import pytest

import telegram._utils.datetime
import telegram._utils.files
from telegram import Animation, InputFile, MessageEntity
from tests.auxil.files import TEST_DATA_PATH, data_file


class TestFiles:
    @pytest.mark.parametrize(
        ("string", "expected"),
        [
            (str(data_file("game.gif")), True),
            (str(TEST_DATA_PATH), False),
            (data_file("game.gif"), True),
            (TEST_DATA_PATH, False),
            ("https:/api.org/file/botTOKEN/document/file_3", False),
            (None, False),
        ],
    )
    def test_is_local_file(self, string: Union[str, Path, None], expected: bool):
        assert telegram._utils.files.is_local_file(string) == expected

    @pytest.mark.parametrize(
        ("string", "expected_local", "expected_non_local"),
        [
            (data_file("game.gif"), data_file("game.gif").as_uri(), InputFile),
            (TEST_DATA_PATH, TEST_DATA_PATH, TEST_DATA_PATH),
            ("file://foobar", "file://foobar", ValueError),
            (str(data_file("game.gif")), data_file("game.gif").as_uri(), InputFile),
            (str(TEST_DATA_PATH), str(TEST_DATA_PATH), str(TEST_DATA_PATH)),
            (
                "https:/api.org/file/botTOKEN/document/file_3",
                "https:/api.org/file/botTOKEN/document/file_3",
                "https:/api.org/file/botTOKEN/document/file_3",
            ),
        ],
        ids=[
            "Path(local_file)",
            "Path(directory)",
            "file_uri",
            "str-path local file",
            "str-path directory",
            "URL",
        ],
    )
    def test_parse_file_input_string(
        self,
        string: Union[str, Path, None],
        expected_local: Union[str, Path, InputFile, ValueError],
        expected_non_local: Union[str, Path, InputFile, ValueError],
    ):
        assert (
            telegram._utils.files.parse_file_input(string, local_mode=True)
            == expected_local
        )

        if expected_non_local is InputFile:
            assert isinstance(
                telegram._utils.files.parse_file_input(string, local_mode=False), InputFile
            )
        elif expected_non_local is ValueError:
            with pytest.raises(ValueError, match="but local mode is not enabled."):
                telegram._utils.files.parse_file_input(string, local_mode=False)
        else:
            assert (
                telegram._utils.files.parse_file_input(string, local_mode=False)
                == expected_non_local
            )

    @pytest.mark.parametrize(
        ("file_like", "filename", "expected"),
        [
            (data_file("game.gif").open("rb"), "test_file", InputFile),
            (data_file
