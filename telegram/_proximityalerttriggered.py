#!/usr/bin/env python

from typing import TYPE_CHECKING, Optional
from telegram._telegramobject import TelegramObject
from telegram._user import User
from telegram._utils.types import JSONDict

if TYPE_CHECKING:
    from telegram import Bot

class ProximityAlertTriggered(TelegramObject):
    """
    This object represents the content of a service message, sent whenever a user in the chat
    triggers a proximity alert set by another user.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`traveler`, :attr:`watcher` and :attr:`distance` are equal.

    Args:
        traveler (User): User that triggered the alert
        watcher (User): User that set the alert
        distance (int): The distance between the users

    Attributes:
        traveler (User): User that triggered the alert
        watcher (User): User that set the alert
        distance (int): The distance between the users

    """
    __slots__ = ("distance", "traveler", "watcher")

    def __init__(
        self,
        traveler: User,
        watcher: User,
        distance: int,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(api_kwargs=api_kwargs)
        self.traveler: User = traveler
        self.watcher: User = watcher
        self.distance: int = distance

        self._id_attrs = (self.traveler, self.watcher, self.distance)

        self._freeze()

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["ProximityAlertTriggered"]:
        """
        Creates an instance of ProximityAlertTriggered from its JSON representation.

        Args:
            data (Optional[JSONDict]): The JSON representation of the ProximityAlertTriggered object.
            bot (Bot): The Bot object associated with this ProximityAlertTriggered object.

        Returns:
            Optional[ProximityAlertTriggered]: An instance of ProximityAlertTriggered, or None if the
            data is None or invalid.
        """
        data = cls._parse_data(data)

        if not data:
            return None

        data["traveler"] = User.de_json(data.get("traveler"), bot)
        data["watcher"] = User.de_json(data.get("watcher"), bot)

        return super().de_json(data=data, bot=bot)
