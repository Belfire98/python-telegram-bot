#!/usr/bin/env python

"""A library that provides a Python interface to the Telegram Bot API

Copyright (C) 2015-2024
Leandro Toledo de Souza <devs@python-telegram-bot.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser Public License for more details.

You should have received a copy of the GNU Lesser Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pytest
from typing import Dict, Any, Union
from telegram import LoginUrl
from tests.auxil.slots import mro_slots


@pytest.fixture(scope="module")
def login_url() -> LoginUrl:
    return LoginUrl(
        url=TestLoginUrlBase.url,
        forward_text=TestLoginUrlBase.forward_text,
        bot_username=TestLoginUrlBase.bot_username,
        request_write_access=TestLoginUrlBase.request_write_access,
    )


class TestLoginUrl:
    """Tests for the `LoginUrl` class."""

    url = "http://www.google.com"
    forward_text = "Send me forward!"
    bot_username = "botname"
    request_write_access = True

    def test_slot_behaviour(self, login_url: LoginUrl):
        """Tests that the `LoginUrl` instance has the correct slots."""
        for attr in login_url.__slots__:
            assert getattr(login_url, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(login_url)) == len(set(mro_slots(login_url))), "duplicate slot"

    def test_to_dict(self, login_url: LoginUrl):
        """Tests that the `LoginUrl` instance can be converted to a dictionary."""
        login_url_dict: Dict[str, Union[str, bool]] = login_url.to_dict()

        assert isinstance(login_url_dict, dict)
        assert login_url_dict["url"] == self.url
        assert login_url_dict["forward_text"] == self.forward_text
        assert login_url_dict["bot_username"] == self.bot_username
        assert login_url_dict["request_write_access"] == self.request_write_access

    def test_equality(self):
        """Tests that the `LoginUrl` instances are compared correctly."""
        a: LoginUrl = LoginUrl(self.url, self.forward_text, self.bot_username, self.request_write_access)
        b: LoginUrl = LoginUrl(self.url, self.forward_text, self.bot_username, self.request_write_access)
        c: LoginUrl = LoginUrl(self.url)
        d: LoginUrl = LoginUrl("text.com", self.forward_text, self.bot_username, self.request_write_access)

        assert a == b
        assert hash(a) == hash(b
