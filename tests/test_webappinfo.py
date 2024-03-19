#!/usr/bin/env python

import pytest
from typing import Dict, Any
from telegram import WebAppInfo
from tests.auxil.slots import mro_slots

class TestWebAppInfo:
    """Tests for the WebAppInfo class."""

    url = "https://www.example.com"
    web_app_info_kwargs = {
        "url": url,
    }

    @pytest.fixture(scope="module")
    def web_app_info(self) -> WebAppInfo:
        """Fixture to create a WebAppInfo instance."""
        return WebAppInfo(**self.web_app_info_kwargs)

    def test_slot_behaviour(self, web_app_info: WebAppInfo) -> None:
        """Test slot behaviour of WebAppInfo instance."""
        for attr in web_app_info.__slots__:
            assert getattr(web_app_info, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(web_app_info)) == len(set(mro_slots(web_app_info))), "duplicate slot"

    def test_to_dict(self, web_app_info: WebAppInfo) -> None:
        """Test converting WebAppInfo instance to a dictionary."""
        web_app_info_dict = web_app_info.to_dict()

        assert isinstance(web_app_info_dict, dict)
        assert web_app_info_dict["url"] == self.url

    def test_de_json(self, bot: Any) -> None:
        """Test deserializing JSON to WebAppInfo instance."""
        json_dict = {"url": self.url}
        web_app_info = WebAppInfo.de_json(json_dict, bot)
        assert web_app_info.api_kwargs == {}

        assert web_app_info.url == self.url

    @pytest.mark.parametrize(
        "other_url, expected",
        [
            (url, True),
            ("", False),
            ("not_url", False),
        ],
    )
    def test_equality(self, other_url: str, expected: bool) -> None:
        """Test equality of WebAppInfo instances."""
        a = WebAppInfo(self.url)
        b = WebAppInfo(other_url)

        assert a == b is expected

