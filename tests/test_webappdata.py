import pytest
from unittest.mock import MagicMock

from telegram import WebAppData
from telegram.bot import Bot
from tests.auxil.slots import mro_slots


class TestWebAppData:
    """Tests for the WebAppData class."""

    data = "data"
    button_text = "button_text"

    @pytest.mark.usefixtures("bot")
    def test_init(self, bot):
        web_app_data = WebAppData(self.data, self.button_text, bot=bot)

        assert web_app_data.data == self.data
        assert web_app_data.button_text == self.button_text
        assert web_app_data.bot == bot

    def test_slot_behaviour(self, web_app_data):
        for attr in web_app_data.__slots__:
            assert getattr(web_app_data, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(web_app_data)) == len(set(mro_slots(web_app_data))), "duplicate slot"

    def test_to_dict(self, web_app_data):
        web_app_data_dict = web_app_data.to_dict()

        assert isinstance(web_app_data_dict, dict)
        assert web_app_data_dict["data"] == self.data
        assert web_app_data_dict["button_text"] == self.button_text

    def test_de_json(self, bot):
        json_dict = {"data": self.data, "button_text": self.button_text}
        web_app_data = WebAppData.de_json(json_dict, bot)
        assert web_app_data.api_kwargs == {}

        assert web_app_data.data == self.data
        assert web_app_data.button_text == self.button_text

    def test_equality_and_hash(self, web_app_data):
        a = WebAppData(self.data, self.button_text)
        b = WebAppData(self.data, self.button_text)
        c = WebAppData("", "")
        d = WebAppData("not_data", "not_button_text")

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)

    def test_json(self, web_app_data):
        json_str = web_app_data.json()

        assert json_str == '{"data": "data", "button_text": "button_text"}'


@pytest.fixture
def web_app_data(bot):
    return WebAppData(data=TestWebAppData.data, button_text=TestWebAppData.button_text, bot=bot)


@pytest.fixture
def bot():
    return MagicMock(spec=Bot)
