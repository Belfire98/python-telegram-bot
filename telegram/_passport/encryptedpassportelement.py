#!/usr/bin/env python

import dataclasses
import json
from collections.abc import Callable
from typing import Any, Final, Literal, NamedTuple, Optional, Sequence, Tuple, Type, Union

from telegram._passport.credentials import decrypt_json
from telegram._passport.data import IdDocumentData, PersonalDetails, ResidentialAddress
from telegram._passport.passportfile import PassportFile
from telegram._telegramobject import TelegramObject
from telegram._utils.argumentparsing import parse_sequence_arg
from telegram._utils.types import JSONDict

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from telegram import Bot, Credentials

from __future__ import annotations

class _IdAttrs(NamedTuple):
    type: str
    data: Optional[Union[PersonalDetails, IdDocumentData, ResidentialAddress]]
    phone_number: Optional[str]
    email: Optional[str]
    files: Tuple[PassportFile, ...]
    front_side: Optional[PassportFile]
    reverse_side: Optional[PassportFile]
    selfie: Optional[PassportFile]

class EncryptedPassportElement(TelegramObject):
    """
    Contains information about documents or other Telegram Passport elements shared with the bot
    by the user. The data has been automatically decrypted by python-telegram-bot.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`type`, :attr:`data`, :attr:`phone_number`, :attr:`email`,
    :attr:`files`, :attr:`front_side` and :attr:`reverse_side` and :attr:`selfie` are equal.

    Note:
        This object is decrypted only when originating from
        :obj:`telegram.PassportData.decrypted_data`.

    Args:
        type (Literal["personal_details", "passport", "driver_license", "identity_card", "internal_passport", "address", "utility_bill", "bank_statement", "rental_agreement", "passport_registration", "temporary_registration", "phone_number", "email"]): Element type.
        hash (str): Base64-encoded element hash for using in
            :class:`telegram.PassportElementErrorUnspecified`.
        data (:class:`telegram.PersonalDetails` | :class:`telegram.IdDocumentData` | \
            :class:`telegram.ResidentialAddress` | :obj:`str`, optional):
            Decrypted or encrypted data; available only for "personal_details",
            "passport", "driver_license", "identity_card", "internal_passport" and "address" types.
        phone_number (:obj:`str`, optional): User's verified phone number; available only for
            "phone_number" type.
        email (:obj:`str`, optional): User's verified email address; available only for "email"
            type.
        files (Sequence[:class:`telegram.PassportFile`], optional): Array of encrypted/decrypted
            files with documents provided by the user; available only for "utility_bill", 
            "bank_statement", "rental_agreement", "passport_registration" and 
            "temporary_registration" types.

            .. versionchanged:: 20.0
                |sequenceclassargs|

        front_side (:class:`telegram.PassportFile`, optional): Encrypted/decrypted file with the
            front side of the document, provided by the user; available only for "passport",
            "driver_license", "identity_card" and "internal_passport".
        reverse_side (:class:`telegram.PassportFile`, optional): Encrypted/decrypted file with the
            reverse side of the document, provided by the user; available only for
            "driver_license" and "identity_card".
        selfie (:class:`telegram.PassportFile`, optional): Encrypted/decrypted file with the
            selfie of the user holding a document, provided by the user; available if requested for 
            "passport", "driver_license", "identity_card" and "internal_passport".
        translation (Sequence[:class:`telegram.PassportFile`], optional): Array of
            encrypted/decrypted files with translated versions of documents provided by the user; 
            available if requested requested for "passport", "driver_license", "identity_card", 
            "internal_passport", "utility_bill", "bank_statement", "rental_agreement", 
            "passport_registration" and "temporary_registration" types.

            .. versionchanged:: 20.0
                |sequenceclassargs|

    Attributes:
        type (:obj:`str`): Element type. One of "personal_details", "passport", "driver_license",
            "identity_card", "internal_passport", "address", "utility_bill", "bank_statement",
            "rental_agreement", "passport_registration", "temporary_registration", "phone_number",
            "email".
        hash (:obj:`str`): Base64-encoded element hash for using in
            :class:`telegram.Passport
