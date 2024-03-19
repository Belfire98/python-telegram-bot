#!/usr/bin/env python

from typing import Optional, Dict, Any, TypeVar, Union
from telegram._telegramobject import TelegramObject
from telegram._utils.types import JSONDict

T = TypeVar('T', bound='Contact')

class Contact(TelegramObject):
    """
    This object represents a phone contact.

    Args:
        phone_number (str): Contact's phone number.
        first_name (str): Contact's first name.
        last_name (Optional[str]): Contact's last name.
        user_id (Optional[int]): Contact's user identifier in Telegram.
        vcard (Optional[str]): Additional data about the contact in the form of a vCard.

    Attributes:
        phone_number (str): Contact's phone number.
        first_name (str): Contact's first name.
        last_name (Optional[str]): Contact's last name.
        user_id (Optional[int]): Contact's user identifier in Telegram.
        vcard (Optional[str]): Additional data about the contact in the form of a vCard.

    """
    __slots__ = ("first_name", "last_name", "phone_number", "user_id", "vcard")

    def __init__(
        self,
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        user_id: Optional[int] = None,
        vcard: Optional[str] = None,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(api_kwargs=api_kwargs)
        # Required
        self.phone_number: str = str(phone_number)
        self.first_name: str = first_name
        # Optionals
        self.last_name: Optional[str] = last_name
        self.user_id: Optional[int] = user_id
        self.vcard: Optional[str] = vcard

        self._id_attrs = (self.phone_number,)

        self._freeze()

    @classmethod
    def de_json(cls: type[T], json_dict: JSONDict, **kwargs: Any) -> T:
        """
        Creates a new Contact object from a JSON dictionary.

        Args:
            json_dict (JSONDict): A dictionary with the JSON encoding of the object.

        Returns:
            A new Contact object.

        """
        return cls(
            phone_number=json_dict['phone_number'],
            first_name=json_dict['first_name'],
            last_name=json_dict.get('last_name'),
            user_id=json_dict.get('user_id'),
            vcard=json_dict.get('vcard'),
            api_kwargs=kwargs,
        )

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the object.

        Returns:
            A string with the object's attributes.

        """
        return f'Contact(phone_number={self.phone_number}, first_name={self.first_name}, ' \
               f'last_name={self.last_name}, user_id={self.user_id}, vcard={self.vcard})'

