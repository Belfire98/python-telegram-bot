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
"""Common base class for media objects with thumbnails"""
from typing import TYPE_CHECKING, Optional, Type, TypeVar, Union

from telegram._files._basemedium import _BaseMedium
from telegram._files.photosize import PhotoSize
from telegram._utils.types import JSONDict

if TYPE_CHECKING:
    from telegram import Bot

# pylint: disable=invalid-name
ThumbedMT_co = TypeVar("ThumbedMT_co", bound="_BaseThumbedMedium", covariant=True)


class _BaseThumbedMedium(_BaseMedium):
    """
    Base class for objects representing the various media file types that may include a thumbnail.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`file_unique_id` is equal.

    Args:
        file_id (str): Identifier for this file, which can be used to download
            or reuse the file.
        file_unique_id (str): Unique identifier for this file, which
            is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
        file_size (Optional[int]): File size.
        thumbnail (Optional[PhotoSize]): Thumbnail as defined by sender.

            .. versionadded:: 20.2

    Attributes:
        file_id (str): File identifier.
        file_unique_id (str): Unique identifier for this file, which
            is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
        file_size (Optional[int]): Optional. File size.
        thumbnail (Optional[PhotoSize]): Optional. Thumbnail as defined by sender.

            .. versionadded:: 20.2

    """

    __slots__ = ("thumbnail",)

    def __init__(
        self,
        file_id: str,
        file_unique_id: str,
        file_size: Optional[int] = None,
        thumbnail: Optional[PhotoSize] = None,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(
            file_id=file_id,
            file_unique_id=file_unique_id,
            file_size=file_size,
            api_kwargs=api_kwargs,
        )

        self.thumbnail: Optional[PhotoSize] = thumbnail

    @classmethod
    def from_file_id_and_thumbnail(
        cls: Type[ThumbedMT_co], file_id: str, thumbnail: Optional[PhotoSize] = None
    ) -> ThumbedMT_co:
        """
        Create an instance of the class from a file_id and thumbnail.

        Args:
            file_id (str): Identifier for the file.
            thumbnail (Optional[PhotoSize]): Thumbnail as defined by sender.

        Returns:
            ThumbedMT_co: An instance of the class with the given file_id and thumbnail.

        """
        return cls(file_id=file_id, file_unique_id=file_id, thumbnail=thumbnail)

    @classmethod
    def de_json(
        cls: Type[ThumbedMT_co], data: Optional[JSONDict], bot: "Bot"
    ) -> Optional[ThumbedMT_co]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if not data:
            return None

        # In case this wasn't already done by the subclass
        if not isinstance(data.get("thumbnail"), PhotoSize):
            data["thumbnail"] = PhotoSize.de_json(data.get("thumbnail"), bot)

        api_kwargs = {}
        # This is a deprecated field that TG still returns for backwards compatibility
        # Let's filter it out to speed up the de-json process
        if data.get("thumb") is not None:
            api_kwargs["thumb"] = data.pop("thumb")

        return super()._de_json(data=data, bot=bot, api_kwargs=api_kwargs)
