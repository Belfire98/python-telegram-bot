#!/usr/bin/env python

"""
A library that provides a Python interface to the Telegram Bot API
"""

import pytest
from telegram import PassportElementErrorReverseSide
from tests.auxil.slots import mro_slots

class TestPassportElementErrorReverseSideBase:
    """
    A base class for testing PassportElementErrorReverseSide
    """
    type_: str
    file_hash: str
    message: str

    def __init__(self, type_: str, file_hash: str, message: str):
        self.type_ = type_
        self.file_hash = file_hash
        self.message = message

