#!/usr/bin/env python

from typing import Any, Callable, Type, TypeVar, Union

from telegram._utils.warnings import warn
from telegram.warnings import PTBDeprecationWarning

T = TypeVar('T')

def build_deprecation_warning_message(
    deprecated_name: str,
    new_name: str,
    object_type: str,
    bot_api_version: str,
) -> str:
    """Builds a warning message for the transition in API when an object is renamed.

    Returns a warning message that can be used in `warn` function.
    """
    return (
        f"The {object_type} '{deprecated_name}' was renamed to '{new_name}' in Bot API "
        f"{bot_api_version}. We recommend using '{new_name}' instead of "
        f"'{deprecated_name}'."
    )

def warn_about_deprecated_arg_return_new_arg(
    deprecated_arg: Union[T, None],
    new_arg: Union[T, None],
    deprecated_arg_name: str,
    new_arg_name: str,
    bot_api_version: str,
    stacklevel: int = 2,
    warn_callback: Callable[[str, Type[Warning], int], None] = warn,
) -> T:
    """A helper function for the transition in API when argument is renamed.

    Checks the `deprecated_arg` and `new_arg` objects; warns if non-None `deprecated_arg` object
    was passed. Returns `new_arg` object (either the one originally passed by the user or the one
    that user passed as `deprecated_arg`).

    Raises `ValueError` if both `deprecated_arg` and `new_arg` objects were passed, and they are
    different.
    """
    if not isinstance(bot_api_version, str):
        raise TypeError("bot_api_version must be a string")
    if not isinstance(stacklevel, int):
        raise TypeError("stacklevel must be an integer")
    if not callable(warn_callback):
        raise TypeError("warn_callback must be a callable")

    if deprecated_arg is not None and new_arg is not None and type(deprecated_arg) != type(new_arg):
        base_message = build_deprecation_warning_message(
            deprecated_name=deprecated_arg_name,
            new_name=new_arg_name,
            object_type="parameter",
            bot_api_version=bot_api_version,
        )
        raise ValueError(
            f"You passed different entities as '{deprecated_arg_name}' and '{new_arg_name}'. "
            f"{base_message}"
        )

    if deprecated_arg is not None:
        warn_callback(
            f"Bot API {bot_api_version} renamed the argument '{deprecated_arg_name}' to "
            f"'{new_arg_name}'.",
            PTBDeprecationWarning,
            stacklevel + 1,
        )
        return deprecated_arg

    return new_arg

def warn_about_deprecated_attr_in_property(
    deprecated_attr_name: str,
    new_attr_name: str,
    bot_api_version: str,
    stacklevel: int = 2,
) -> None:
    """A helper function for the transition in API when attribute is renamed. Call from properties.

    The properties replace deprecated attributes in classes and issue these deprecation warnings.
    """
    if not isinstance(bot_api_version, str):
        raise TypeError("bot_api_version must be a string")
    if not isinstance(stacklevel, int):
        raise TypeError("stacklevel must be an integer")

    warn(
        f"Bot API {bot_api_version} renamed the attribute '{deprecated_attr_name}' to "
        f"'{new_attr_name}'.",
        PTBDeprecationWarning,
        stacklevel=stacklevel + 1,
    )
