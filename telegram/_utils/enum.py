#!/usr/bin/env python

import enum as _enum
import sys
from typing import Type, TypeVar, Union

_A = TypeVar("_A")
_B = TypeVar("_B")
_Enum = TypeVar("_Enum", bound=_enum.Enum)


def get_member(enum_cls: Type[_Enum], value: _A, default: _B) -> Union[_Enum, _A, _B]:
    """Tries to call ``enum_cls(value)`` to convert the value into an enumeration member.
    If that fails, the ``default`` is returned.
    """
    try:
        return enum_cls(value)
    except ValueError:
        return default


class StringEnum(str, _enum.Enum):
    """Helper class for string enums where ``str(member)`` prints the value, but ``repr(member)``
    gives ``EnumName.MEMBER_NAME``.
    """

    __slots__ = ()

    def __repr__(self) -> str:
        """Returns a string representation of the enum member in the format:
        ``<EnumName.MEMBER_NAME>``.
        """
        return f"<{self.__class__.__name__}.{self.name}>"

    def __str__(self) -> str:
        """Returns the value of the enum member as a string."""
        return str(self)

    def __eq__(self, other: object) -> bool:
        """Compares the enum member with another object for equality."""
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash value of the enum member."""
        return hash(self.value)


class IntEnum(_enum.IntEnum):
    """Helper class for int enums where ``str(member)`` prints the value, but ``repr(member)``
    gives ``EnumName.MEMBER_NAME``.
    """

    __slots__ = ()

    def __repr__(self) -> str:
        """Returns a string representation of the enum member in the format:
        ``<EnumName.MEMBER_NAME>``.
        """
        return f"<{self.__class__.__name__}.{self.name}>"

    def __str__(self) -> str:
        """Returns the value of the enum member as a string."""
        if sys.version_info < (3, 11):
            return str(self.value)
        return super().__str__()

    def __eq__(self, other: object) -> bool:
        """Compares the enum member with another object for equality."""
        if isinstance(other, int):
            return self.value == other
        return super().__eq__(other)

    def __hash__(self) -> int:
        """Returns the hash value of the enum member."""
        return hash(self.value)
