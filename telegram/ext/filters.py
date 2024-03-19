#!/usr/bin/env python

import re
from abc import ABC, abstractmethod
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    FrozenSet,
    Iterable,
    List,
    Match,
    NamedTuple,
    Optional,
    Pattern,
    Set,
    Tuple,
    Type,
    Union,
)

from telegram import (
    Chat as TGChat,
    Message,
    MessageEntity,
    MessageOriginChannel,
    MessageOriginChat,
    MessageOriginUser,
    Update,
)
from telegram import User as TGUser
from telegram._utils.types import SCT
from telegram.constants import DiceEmoji as DiceEmojiEnum
from telegram.ext._utils._update_parsing import parse_chat_id, parse_username
from telegram.ext._utils.types import FilterDataDict


class BaseFilter(ABC):
    """Base class for all Filters.

    Filters subclassing from this class can combined using bitwise operators:

    And::

        filters.TEXT & filters.Entity(MENTION)

    Or::

        filters.AUDIO | filters.VIDEO

    Exclusive Or::

        filters.Regex(r'(a?x)') ^ filters.Regex(r'(b?x)')

    Not::

        ~ filters.COMMAND

    Also works with more than two filters::

        filters.TEXT & (filters.Entity("url") | filters.Entity("text_link"))
        filters.TEXT & (~ filters.FORWARDED)

    Note:
        Filters use the same short circuiting logic as python's :keyword:`and`, :keyword:`or` and
        :keyword:`not`. This means that for example::

            filters.Regex(r'(a?x)') | filters.Regex(r'(b?x)')

        With ``message.text == 'x'``, will only ever return the matches for the first filter,
        since the second one is never evaluated.

    If you want to create your own filters create a class inheriting from either
    :class:`MessageFilter` or :class:`UpdateFilter` and implement a ``filter()``
    method that returns a boolean: :obj:`True` if the message should be
    handled, :obj:`False` otherwise.
    Note that the filters work only as class instances, not actual class objects (so remember to
    initialize your filter classes).

    By default, the filters name (what will get printed when converted to a string for display)
    will be the class name. If you want to overwrite this assign a better name to the :attr:`name`
    class variable.

    .. versionadded:: 20.0
        Added the arguments :attr:`name` and :attr:`data_filter`.

    Args:
        name (:obj:`str`): Name for this filter. Defaults to the type of filter.
        data_filter (:obj:`bool`): Whether this filter is a data filter. A data filter should
            return a dict with lists. The dict will be merged with
            :class:`telegram.ext.CallbackContext`'s internal dict in most cases
            (depends on the handler).
    """

    __slots__ = ("_data_filter", "_name")

    def __init__(self, name: Optional[str] = None, data_filter: bool = False):
        self._name = self.__class__.__name__ if name is None else name
        self._data_filter = data_filter

    def __and__(self, other: "BaseFilter") -> "BaseFilter":
        """Defines `AND` bitwise operator for :class:`BaseFilter` object.
        The combined filter accepts an update only if it is accepted by both filters.
        For example, ``filters.PHOTO & filters.CAPTION`` will only accept messages that contain
        both a photo and a caption.

        Returns:
           :obj:`BaseFilter`
        """
        return _MergedFilter(self, and_filter=other)

    def __or__(self, other: "BaseFilter") -> "BaseFilter":
        """Defines `OR` bitwise operator for :class:`BaseFilter` object.
        The combined filter accepts an update only if it is accepted by any of the filters.
        For example, ``filters.PHOTO | filters.CAPTION`` will only accept messages that contain
        photo or caption or both.

        Returns:
           :obj:`BaseFilter`
        """
        return _MergedFilter(self, or_filter=other)

    def __xor__(self, other: "BaseFilter") -> "BaseFilter":
        """Defines `XOR` bitwise operator for :class:`BaseFilter` object.
        The combined filter accepts an update only if it is accepted by any of the filters and
        not both of them. For example, ``filters.PHOTO ^ filters.CAPTION`` will only accept
        messages that contain photo or caption, not both of them.

        Returns:
           :obj:`BaseFilter`
        """
        return _XORFilter(self, other)

    def __invert__(self) -> "BaseFilter":
        """Defines `NOT` bitwise operator for :class:`BaseFilter` object.
        The combined filter accepts an update only if it is accepted by any of the filters.
        For example, ``~ filters.PHOTO`` will only accept messages that do not contain photo.

        Returns:
           :obj:`BaseFilter`
        """
        return _InvertedFilter(self)

    def __repr__(self) -> str:
        """Gives name for this filter.

        .. seealso::
               :meth:`name`

        Returns:
            :obj:`str`:
        """
        return self.name

    @property
    def data_filter(self) -> bool:
        """:obj:`bool`: Whether this filter is a data filter."""
        return self._
