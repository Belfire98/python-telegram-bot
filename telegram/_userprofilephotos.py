#!/usr/bin/env python

from typing import Any, List, Optional, Tuple, Type, Union

import json

from telegram._files.photosize import PhotoSize
from telegram._telegramobject import TelegramObject
from telegram._utils.types import JSONDict

if TYPE_CHECKING:
    from telegram import Bot

    PhotoSizeType = Type[PhotoSize]
else:
    PhotoSizeType = Any


class UserProfilePhotos(TelegramObject):
    """This object represents a user's profile pictures.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`total_count` and :attr:`photos` are equal.

    Args:
        total_count (int): Total number of profile pictures the target user has.
        photos (List[List[PhotoSize]]): Requested profile pictures (in up to 4 sizes each).

            .. versionchanged:: 20.0
                |sequenceclassargs|

    Attributes:
        total_count (int): Total number of profile pictures.
        photos (Tuple[Tuple[PhotoSize, ...], ...]): Requested profile pictures (in up to 4
            sizes each).

            .. versionchanged:: 20.0
                |tupleclassattrs|

    """

    __slots__ = ("photos", "total_count")

    def __init__(
        self,
        total_count: int,
        photos: List[List[PhotoSize]],
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(**api_kwargs)
        # Required
        self.total_count: int = total_count
        self.photos: Tuple[Tuple[PhotoSize, ...], ...] = tuple(tuple(sizes) for sizes in photos)

        self._id_attrs = (self.total_count, self.photos)

        self._freeze()

    @property
    def total_count(self) -> int:
        """int: Total number of profile pictures."""
        return self._total_count

    @total_count.setter
    def total_count(self, total_count: int) -> None:
        if not isinstance(total_count, int):
            raise TypeError("total_count must be an integer")
        self._total_count = total_count

    @property
    def photos(self) -> Tuple[Tuple[PhotoSize, ...], ...]:
        """Tuple[Tuple[PhotoSize, ...], ...]: Requested profile pictures (in up to 4 sizes each)."""
        return self._photos

    @photos.setter
    def photos(self, photos: List[List[PhotoSize]]) -> None:
        if not all(isinstance(photo, Iterable) and all(isinstance(p, PhotoSize) for p in photo) for photo in photos):
            raise TypeError("photos must be a list of lists of PhotoSize objects")
        self._photos = tuple(tuple(sizes) for sizes in photos)

    @classmethod
    def de_json(cls: Type["UserProfilePhotos"], data: Optional[JSONDict], bot: "Bot") -> Optional["UserProfilePhotos"]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if not data:
            return None

        data["photos"] = [
            [PhotoSize.de_json(photo, bot) for photo in photo_list] for photo_list in data["photos"]
        ]

        return super().de_json(data=data, bot=bot)

