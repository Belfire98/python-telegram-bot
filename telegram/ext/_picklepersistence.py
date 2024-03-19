import pickle
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Set, Tuple, Type, TypeVar, Union

from telegram import Bot, TelegramObject
from telegram._utils.types import FilePathInput
from telegram._utils.warnings import warn
from telegram.ext import BasePersistence, PersistenceInput
from telegram.ext._contexttypes import ContextTypes
from telegram.ext._utils.types import BD, CD, UD, CDCData, ConversationDict, ConversationKey

_REPLACED_KNOWN_BOT = "a known bot replaced by PTB's PicklePersistence"
_REPLACED_UNKNOWN_BOT = "an unknown bot replaced by PTB's PicklePersistence"

TelegramObj = TypeVar("TelegramObj", bound=TelegramObject)


def _all_subclasses(cls: Type[TelegramObj]) -> Set[Type[TelegramObj]]:
    """Gets all subclasses of the specified object, recursively."""
    subclasses = cls.__subclasses__()
    return set(subclasses).union([s for c in subclasses for s in _all_subclasses(c)])


def _reconstruct_to(cls: Type[TelegramObj], kwargs: dict) -> TelegramObj:
    """
    This method is used for unpickling. The data, which is in the form a dictionary, is
    converted back into a class. Works mostly the same as :meth:`TelegramObject.__setstate__`.
    This function should be kept in place for backwards compatibility even if the pickling logic
    is changed, since `_custom_reduction` places references to this function into the pickled data.
    """
    obj = cls.__new__(cls)
    obj.__setstate__(kwargs)
    return obj


def _custom_reduction(cls: TelegramObj) -> Tuple[Callable, Tuple[Type[TelegramObj], dict]]:
    """
    This method is used for pickling. The bot attribute is preserved so _BotPickler().persistent_id
    works as intended.
    """
    data = cls._get_attrs(include_private=True)  # pylint: disable=protected-access
    # MappingProxyType is not pickable, so we convert it to a dict
    # no need to convert back to MPT in _reconstruct_to, since it's done in __setstate__
    data["api_kwargs"] = dict(data["api_kwargs"])  # type: ignore[arg-type]
    return _reconstruct_to, (cls.__class__, data)


class _BotPickler(pickle.Pickler):
    __slots__ = ("_bot",)

    def __init__(self, bot: Bot, *args: Any, **kwargs: Any):
        self._bot = bot
        super().__init__(*args, **kwargs)

    def reducer_override(
        self, obj: TelegramObj
    ) -> Tuple[Callable, Tuple[Type[TelegramObj], dict]]:
        """
        This method is used for pickling. The bot attribute is preserved so
        _BotPickler().persistent_id works as intended.
        """

