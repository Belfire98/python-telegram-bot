#!/usr/bin/env python
#
#  A library that provides a Python interface to the Telegram Bot API
#  Copyright (C) 2015-2024
#  Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser Public License for more details.
#
#  You should have received a copy of the GNU Lesser Public License
#  along with this program.  If not, see [http://www.gnu.org/licenses/].

def get_private_key():
    """Prompts the user to enter their RSA private key."""
    return input("Please enter your RSA private key: ")

# PRIVATE_KEY = get_private_key()  # Uncomment this line when running the code
PRIVATE_KEY = b"""-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----"""  # Replace this with your own private key
