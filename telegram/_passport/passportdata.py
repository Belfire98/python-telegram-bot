#!/usr/bin/env python

import typing as ty

from telegram._passport.credentials import EncryptedCredentials
from telegram._passport.encryptedpassportelement import EncryptedPassportElement
from telegram._telegramobject import TelegramObject
from telegram._utils.argumentparsing import parse_sequence_arg
from telegram._utils.types import JSONDict

if ty.TYPE_CHECKING:
    from telegram import Bot, Credentials


class PassportData(TelegramObject):
    """Information about Telegram Passport data shared with the bot by the user.

    Args:
        data (Sequence[:class:`telegram.EncryptedPassportElement`]): Array with encrypted
            information about documents and other Telegram Passport elements that was shared with
            the bot.

            .. versionchanged:: 20.0
                |sequenceclassargs|

        credentials (:class:`telegram.EncryptedCredentials`)): Encrypted credentials.

    Attributes:
        data (Tuple[:class:`telegram.EncryptedPassportElement`]): Array with encrypted
            information about documents and other Telegram Passport elements that was shared with
            the bot.

            .. versionchanged:: 20.0
                |tupleclassattrs|

        credentials (:class:`telegram.EncryptedCredentials`): Encrypted credentials.

    """

    __slots__ = ("_decrypted_data", "credentials", "data")

    def __init__(
        self,
        data: ty.Sequence[EncryptedPassportElement],
        credentials: EncryptedCredentials,
    ):
        """Initialize a PassportData instance."""
        super().__init__()

        self.data: ty.Tuple[EncryptedPassportElement, ...] = parse_sequence_arg(data)
        self.credentials: EncryptedCredentials = credentials

        self._decrypted_data: ty.Optional[ty.Tuple[EncryptedPassportElement]] = None
        self._id_attrs = tuple([x.type for x in data] + [credentials.hash])

        self._freeze()

    @classmethod
    def de_json(cls, data: ty.Optional[JSONDict], bot: "Bot") -> ty.Optional["PassportData"]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if not data:
            return None

        data["data"] = EncryptedPassportElement.de_list(data.get("data"), bot)
        data["credentials"] = EncryptedCredentials.de_json(data.get("credentials"), bot)

        return super().de_json(data=data, bot=bot)

    def to_dict(self) -> JSONDict:
        """Return a dictionary representation of the PassportData instance."""
        data = super().to_dict()
        data["data"] = [element.to_dict() for element in self.data]
        data["credentials"] = self.credentials.to_dict()
        return data

    @classmethod
    def from_dict(cls, data: JSONDict, bot: "Bot") -> "PassportData":
        """Create a PassportData instance from a dictionary."""
        data["data"] = EncryptedPassportElement.de_list(data.get("data"), bot)
        data["credentials"] = EncryptedCredentials.de_json(data.get("credentials"), bot)
        return cls(data["data"], data["credentials"])

    @property
    def decrypted_data(self) -> ty.Tuple[EncryptedPassportElement, ...]:
        """
        Tuple[:class:`telegram.EncryptedPassportElement`]: Lazily decrypt and return information
            about documents and other Telegram Passport elements which were shared with the bot.

        .. versionchanged:: 20.0
            Returns a tuple instead of a list.

        Raises:
            telegram.error.PassportDecryptionError: Decryption failed. Usually due to bad
                private/public key but can also suggest malformed/tampered data.
        """
        if self._decrypted_data is None:
            self._decrypted_data = tuple(
                EncryptedPassportElement.de_json_decrypted(
                    element.to_dict(), self.get_bot(), self.decrypted_credentials
                )
                for element in self.data
            )
        return self._decrypted_data  # type: ignore[return-value]

    @property
    def decrypted_credentials(self) -> "Credentials":
        """
        :class:`telegram.Credentials`: Lazily decrypt and return credentials that were used
            to decrypt the data. This object also contains the user specified payload as
            `decrypted_data.payload`.

        Raises:
            telegram.error.PassportDecryptionError: Decryption failed. Usually due to bad
                private/public key but can also suggest malformed/tampered data.
        """
        return self.credentials.decrypted_data
