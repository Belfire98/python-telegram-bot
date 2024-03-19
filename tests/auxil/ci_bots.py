#!/usr/bin/env python

import base64
import json
import os
import random

# ... (rest of the code remains the same)

class BotInfoProvider:
    def __init__(self):
        self._cached = {}
        self.fallbacks = json.loads(base64.b64decode(FALLBACKS).decode("utf-8"))  # type: List[dict[str, str]]

    def _get_value(self, key, fallback):
        if GITHUB_ACTION is not None and BOTS is not None and JOB_INDEX is not None:
            try:
                return BOTS[JOB_INDEX][key]
            except (IndexError, KeyError):
                pass

        return fallback

    def get_bot_info(self):
        if not self._cached:
            self._cached = {k: self._get_value(k, v) for k, v in random.choice(self.fallbacks).items()}

        return self._cached

BOT_INFO_PROVIDER = BotInfoProvider()

def get_bot_info():
    """Get the bot info from the cache or fetch it from the fallback"""
    return BOT_INFO_PROVIDER.get_bot_info()

# ... (rest of the code remains the same)
