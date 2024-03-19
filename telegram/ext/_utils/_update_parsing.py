#!/usr/bin/env python

from typing import FrozenSet, Optional, Union

from telegram._utils.types import SCT

def parse_chat_or_username(
    value: Optional[SCT[Union[int, str]]],
) -> FrozenSet[Union[int, str]]:
    """Accepts a chat ID, username, or collection of chat IDs and usernames
    and returns a frozenset of unique chat IDs and usernames.

    Strips the leading '@' from usernames if present.

    Args:
        value (Optional[SCT[Union[int, str]]]): A chat ID, username, or collection
            of chat IDs and usernames.

    Returns:
        FrozenSet[Union[int, str]]: A frozenset of unique chat IDs and usernames.

    Raises:
        ValueError: If the input value is invalid.
    """
    if value is None:
        return frozenset()

    result = set()
    for item in value:
        if isinstance(item, int):
            result.add(item)
        elif isinstance(item, str):
            if item.startswith("@"):
                item = item[1:]
            if item.isdigit():
                result.add(int(item))
            else:
                result.add(item)
        else:
            raise ValueError(f"Invalid value: {item}")

    return frozenset(result)
