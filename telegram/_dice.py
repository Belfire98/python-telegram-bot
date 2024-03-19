#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2024
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains an object that represents a Telegram Dice."""
from typing import Any, ClassVar, Dict, Final, List, Optional, TypeVar, Union

from telegram import constants
from telegram._telegramobject import TelegramObject
from telegram._utils.types import JSONDict


class Dice(TelegramObject):
    """
    This object represents an animated emoji with a random value for currently supported base
    emoji. (The singular form of "dice" is "die". However, PTB mimics the Telegram API, which uses
    the term "dice".)

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`value` and :attr:`emoji` are equal.

    Note:
        If :attr:`emoji` is :tg-const:`telegram.Dice.DARTS`, a value of 6 currently
        represents a bullseye, while a value of 1 indicates that the dartboard was missed.
        However, this behaviour is undocumented and might be changed by Telegram.

        If :attr:`emoji` is :tg-const:`telegram.Dice.BASKETBALL`, a value of 4 or 5
        currently score a basket, while a value of 1 to 3 indicates that the basket was missed.
        However, this behaviour is undocumented and might be changed by Telegram.

        If :attr:`emoji` is :tg-const:`telegram.Dice.FOOTBALL`, a value of 4 to 5
        currently scores a goal, while a value of 1 to 3 indicates that the goal was missed.
        However, this behaviour is undocumented and might be changed by Telegram.

        If :attr:`emoji` is :tg-const:`telegram.Dice.BOWLING`, a value of 6 knocks
        all the pins, while a value of 1 means all the pins were missed.
        However, this behaviour is undocumented and might be changed by Telegram.

        If :attr:`emoji` is :tg-const:`telegram.Dice.SLOT_MACHINE`, each value
        corresponds to a unique combination of symbols, which
        can be found in our
        :wiki:`wiki <Code-snippets#map-a-slot-machine-dice-value-to-the-corresponding-symbols>`.
        However, this behaviour is undocumented and might be changed by Telegram.

    ..
        In args, some links for limits of `value` intentionally point to constants for only
        one emoji of a group to avoid duplication. For example, maximum value for Dice, Darts and
        Bowling is linked to a constant for Bowling.

    Args:
        value (:obj:`int`): Value of the dice.
            :tg-const:`telegram.Dice.MIN_VALUE`-:tg-const:`telegram.Dice.MAX_VALUE_BOWLING`
            for :tg-const:`telegram.Dice.DICE`, :tg-const:`telegram.Dice.DARTS` and
            :tg-const:`telegram.Dice.BOWLING` base emoji,
            :tg-const:`telegram.Dice.MIN_VALUE`-:tg-const:`telegram.Dice.MAX_VALUE_BASKETBALL`
            for :tg-const:`telegram.Dice.BASKETBALL` and :tg-const:`telegram.Dice.FOOTBALL`
            base emoji,
            :tg-const:`telegram.Dice.MIN_VALUE`-:tg-const:`telegram.Dice.MAX_VALUE_SLOT_MACHINE`
            for :tg-const:`telegram.Dice.SLOT_MACHINE` base emoji.
        emoji (:obj:`str`): Emoji on which the dice throw animation is based.

    Attributes:
        value (:obj:`int`): Value of the dice.
            :tg-const:`telegram.Dice.MIN_VALUE`-:tg-const:`telegram.Dice.MAX_VALUE_BOWLING`
            for :tg-const:`telegram.Dice.DICE`, :tg-const:`telegram.Dice.DARTS` and
            :tg-const:`telegram.Dice.BOWLING` base emoji,
            :tg-const:`telegram.Dice.MIN_VALUE`-:tg-const:`telegram.Dice.MAX_VALUE_BASKETBALL`
            for :tg-const:`telegram.Dice.BASKETBALL` and :tg-const:`telegram.Dice.FOOTBALL`
            base emoji,
            :tg-const:`telegram.Dice.MIN_VALUE`-:tg-const:`telegram.Dice.MAX_VALUE_SLOT_MACHINE`
            for :tg-const:`telegram.Dice.SLOT_MACHINE` base emoji.
        emoji (:obj:`str`
