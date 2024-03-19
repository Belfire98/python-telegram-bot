#!/usr/bin/env python
from dataclasses import dataclass, field
from typing import List, Optional


def warn(message: str, category: type = UserWarning, stacklevel: int = 2):
    raise DeprecationWarning(message) from None


@dataclass
class TelegramObject:
    """Baseclass for all Telegram objects."""

    @classmethod
    def from_dict(cls, data: JSONDict) -> "TelegramObject":
        """Create an instance of the class from a dictionary."""
        raise NotImplementedError

    def to_dict(self) -> JSONDict:
        """Create a dictionary representation of the instance."""
        raise NotImplementedError

    def _freeze(self):
        """Freeze the instance to prevent further modifications."""
        pass


@dataclass
class PassportElementError(TelegramObject):
    """Baseclass for the PassportElementError* classes.

    This object represents an error in the Telegram Passport element which was submitted that
    should be resolved by the user.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`source` and :attr:`type` are equal.

    Args:
        source (str): Error source.
        type (str): The section of the user's Telegram Passport which has the error.
        message (str): Error message.

    Attributes:
        source (str): Error source.
        type (str): The section of the user's Telegram Passport which has the error.
        message (str): Error message.

    """

    source: str
    type: str
    message: str
    _id_attrs: tuple = field(init=False, repr=False)

    def __post_init__(self):
        self._id_attrs = (self.source, self.type)
        self._freeze()


@dataclass
class PassportElementErrorDataField(PassportElementError):
    """
    Represents an issue in one of the data fields that was provided by the user. The error is
    considered resolved when the field's value changes.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`source`, :attr:`type`, :attr:`field_name`,
    :attr:`data_hash` and :attr:`message` are equal.

    Args:
        type (str): The section of the user's Telegram Passport which has the error, one of
            ``"personal_details"``, ``"passport"``, ``"driver_license"``, ``"identity_card"``,
            ``"internal_passport"``, ``"address"``.
        field_name (str): Name of the data field which has the error.
        data_hash (str): Base64-encoded data hash.
        message (str): Error message.

    Attributes:
        type (str): The section of the user's Telegram Passport which has the error, one of
            ``"personal_details"``, ``"passport"``, ``"driver_license"``, ``"identity_card"``,
            ``"internal_passport"``, ``"address"``.
        field_name (str): Name of the data field which has the error.
        data_hash (str): Base64-encoded data hash.
        message (str): Error message.

    """

    type: str
    field_name: str
    data_hash: str
    message: str

    def __post_init__(self):
        self._id_attrs = (self.source, self.type, self.field_name, self.data_hash, self.message)


@dataclass
class PassportElementErrorFile(PassportElementError):
    """
    Represents an issue with a document scan. The error is considered resolved when the file with
    the document scan changes.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`source`, :attr:`type`, :attr:`file_hash`, and
    :attr:`message` are equal.

    Args:
        type (str): The section of the user's Telegram Passport which has the issue, one of
            ``"utility_bill"``, ``"bank_statement"``, ``"rental_agreement"``,
            ``"passport_registration"``, ``"temporary_registration"``.
        file_hash (str): Base64-encoded file hash.
        message (str): Error message.

    Attributes:
        type (str): The section of the user's Telegram Passport which has the issue, one of
            ``"utility_bill"``, ``"bank_statement"``, ``"rental_agreement"``,
            ``"passport_registration"``, ``"temporary_registration"``.
        file_hash (str): Base64-encoded file hash.
        message (str): Error message.

    """

    type: str
    file_hash: str
    message: str

    def __post_init__(self):
        self._id_attrs = (self.source, self.type, self.file_hash, self.message)


@dataclass
class PassportElementErrorFiles(PassportElementError):
    """
    Represents an issue with
