#!/usr/bin/env python

"""This module contains a helper function for Telegram's ReplyMarkups.

.. versionchanged:: 20.0
   Previously, the contents of this module were available through the (no longer existing)
   class ``telegram.ReplyMarkup``.

Warning:
    Contents of this module are intended to be used internally by the library and *not* by the
    user. Changes to this module are not considered breaking changes and may not be documented in
    the changelog.
"""
from collections.abc import Sequence
from typing import Any


def is_keyboard_of_correct_type(keyboard: Any) -> bool:
    """Checks if the keyboard provided is of the correct type - A sequence of sequences.

    Each row in the keyboard must be a sequence of buttons, where each button is a string or a
    single-element sequence.

    Returns:
        bool: True if the keyboard is of the correct type, False otherwise.
    """
    if not isinstance(keyboard, Sequence) or isinstance(keyboard, (str, bytes)):
        return False

    if len(keyboard) < 1 or any(len(row) < 1 for row in keyboard):
        return False

    for row in keyboard:
        if not isinstance(row, Sequence) or isinstance(row, (str, bytes)):
            return False
        for inner in row:
            if not (isinstance(inner, str) or (isinstance(inner, Sequence) and len(inner) == 1 and isinstance(inner[0], str))):
                return False
    return True
