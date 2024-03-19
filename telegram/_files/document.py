#!/usr/bin/env python

from typing import Dict, Optional

from telegram._files._basethumbedmedium import _BaseThumbedMedium
from telegram._files.photosize import PhotoSize
from telegram._utils.types import JSONDict

class Document(_BaseThumbedMedium):
    """This object represents a general file
    (as opposed to photos, voice messages and audio files).

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`file_unique_id` is equal.

    Args:
        file_id (str): Identifier for this file, which can be used to download
            or reuse the file.
        file_unique_id (str): Unique identifier for this file, which is supposed to be
            the same over time and for different bots. Can't be used to download or reuse the file.
        file_name (Optional[str]): Original filename as defined by sender.
        mime_type (Optional[str]): MIME type of the file as defined by sender.
        file_size (Optional[int]): File size in bytes.
        thumbnail (Optional[PhotoSize]): Document thumbnail as defined by sender.

            .. versionadded:: 20.2

    Attributes:
        file_id (str): Identifier for this file, which can be used to download
            or reuse the file.
        file_unique_id (str): Unique identifier for this file, which is supposed to be
            the same over time and for different bots. Can't be used to download or reuse the file.
        file_name (Optional[str]): Optional. Original filename as defined by sender.
        mime_type (Optional[str]): Optional. MIME type of the file as defined by sender.
        file_size (Optional[int]): Optional. File size in bytes.
        thumbnail (Optional[PhotoSize]): Optional. Document thumbnail as defined by sender.

            .. versionadded:: 20.2

    """

    __slots__ = ("file_name", "mime_type")

    def __init__(
        self,
        file_id: str,
        file_unique_id: str,
        file_name: Optional[str] = None,
        mime_type: Optional[str] = None,
        file_size: Optional[int] = None,
        thumbnail: Optional[PhotoSize] = None,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(
            file_id=file_id,
            file_unique_id=file_unique_id,
            file_size=file_size,
            thumbnail=thumbnail,
            api_kwargs=api_kwargs,
        )
        self.file_name: Optional[str] = file_name
        self.mime_type: Optional[str] = mime_type

    def __repr__(self):
        """Return a string representation of the object."""
        attrs = [
            f"{k}={repr(v)}" for k, v in self.__dict__.items() if not k.startswith("_")
        ]
        return f"Document({', '.join(attrs)})"

    @classmethod
    def from_dict(cls, data: Dict):
        """Create a new Document object from a dictionary.

        Args:
            data (Dict): A dictionary representing the Document object.

        Returns:
            Document: A new Document object.

        """
        return cls(
            file_id=data["file_id"],
            file_unique_id=data["file_unique_id"],
            file_name=data.get("file_name"),
            mime_type=data.get("mime_type"),
            file_size=data.get("file_size"),
            thumbnail=PhotoSize.from_dict(data.get("thumbnail")) if data.get("thumbnail") else None,
            api_kwargs=data.get("api_kwargs"),
        )

    def to_dict(self):
        """Create a dictionary representation of the object.

        Returns:
            Dict: A dictionary representing the Document object.

        """
        data = {
            "file_id": self.file_id,
            "file_unique_id": self.file_unique_id,
            "file_size": self.file_size,
            "thumbnail": self.thumbnail.to_dict() if self.thumbnail else None,
            "api_kwargs": self.api_kwargs,
        }
        if self.file_name is not None:
            data["file_name"] = self.file_name
        if self.mime_type is not None:
            data["mime_type"] = self.mime_type
        return data
