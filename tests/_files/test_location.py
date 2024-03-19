import asyncio
import typing

import pytest
from telegram import Location, ParseMode, ReplyParameters
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.request import RequestData


class TestLocationWithoutRequest:
    """Tests for the `Location` class without a request object."""

    latitude = -23.691288
    longitude = -46.788279
    horizontal_accuracy = 999
    live_period = 60
    heading = 90
    proximity_alert_radius = 50

    def test_slot_behaviour(self, location: Location) -> None:
        """Test that the `Location` instance has no extra slots."""
        for attr in location.__slots__:
            assert getattr(location, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(location)) == len(set(mro_slots(location))), "duplicate slot"

    def test_de_json(self, bot: "TelegramBot") -> None:
        """Test that the `Location` instance can be deserialized from JSON."""
        json_dict = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "horizontal_accuracy": self.horizontal_accuracy,
            "live_period": self.live_period,
            "heading": self.heading,
            "proximity_alert_radius": self.proximity_alert_radius,
        }
        location = Location.de_json(json_dict, bot)
        assert location.api_kwargs == {}

        assert location.latitude == self.latitude
        assert location.longitude == self.longitude
        assert location.horizontal_accuracy == self.horizontal_accuracy
        assert location.live_period == self.live_period
        assert location.heading == self.heading
        assert location.proximity_alert_radius == self.proximity_alert_radius

    def test_to_dict(self, location: Location) -> None:
        """Test that the `Location` instance can be serialized to a dictionary."""
        location_dict = location.to_dict()

        assert location_dict["latitude"] == location.latitude
        assert location_dict["longitude"] == location.longitude
        assert location_dict["horizontal_accuracy"] == location.horizontal_accuracy
        assert location_dict["live_period"] == location.live_period
        assert location_dict["heading"] == location.heading
        assert location_dict["proximity_alert_radius"] == location.proximity_alert_radius

    def test_equality(self) -> None:
        """Test that the `Location` instances are equal if their latitude and longitude are equal."""
        a = Location(self.longitude, self.latitude)
        b = Location(self.longitude, self.latitude)
        d = Location(0, self.latitude)

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a != d
        assert hash(a) != hash(d)


class TestLocationWithRequest:
    """Tests for the `Location` class with a request object."""

    @pytest.mark.parametrize(
        ("default_bot", "custom"),
        [
            ({"allow_sending_without_reply": True}, None),
            ({"allow_sending_without_reply": False}, None),
            ({"allow_sending_without_reply": False}, True),
        ],
        indirect=["default_bot"],
    )
    async def test_send_location_default_allow_sending_without_reply(
        self,
        default_bot: "TelegramBot",
        chat_id: int,
        location: Location,
        custom: typing.Optional[bool],
    ) -> None:
        """
        Test that the `send_location` method of the `TelegramBot` class uses the
        `allow_sending_without_reply` argument correctly.
        """
        reply_to_message = await default_bot.send_message(chat_id, "test")
        await reply_to_message.delete()
        if custom is not None:
            message = await default_bot.send_location(
                chat_id,
                location=location,
                allow_sending_without_reply=custom,
                reply_to_message_id=reply_to_message.message_id,
            )
            assert message.reply_to_message is None
        elif default_bot.defaults.allow_sending_without_reply:
            message = await default_bot.send_location(
                chat_id, location=location, reply_to_message_id=reply_to_message.message_id
            )
            assert message.reply_to_message is None
        else:
            with pytest.raises(BadRequest, match="Message to reply not found"):
                await default_bot.send_location(
                    chat_id, location=location, reply_to_message_id=reply_to_message.message_id
                )

    @pytest.mark.parametri
