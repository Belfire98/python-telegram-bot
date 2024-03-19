#!/usr/bin/env python

import inspect
from copy import deepcopy
import pytest

from telegram import (
    BotCommand,
    Dice,
    ReactionCount,
    ReactionType,
    ReactionTypeCustomEmoji,
    ReactionTypeEmoji,
    ReactionEmoji,
)

ignored = ["self", "api_kwargs"]


class ReactionTypeDefaults:
    custom_emoji_id = "123custom"
    emoji = ReactionEmoji.THUMBS_UP


def reaction_type_custom_emoji(custom_emoji_id=ReactionTypeDefaults.custom_emoji_id):
    return ReactionTypeCustomEmoji(custom_emoji_id)


def reaction_type_emoji(emoji=ReactionTypeDefaults.emoji):
    return ReactionTypeEmoji(emoji)


def make_json_dict(instance: ReactionType, include_optional_args: bool = False) -> dict:
    json_dict = {"type": instance.type}
    sig = inspect.signature(instance.__class__.__init__)

    for param in sig.parameters.values():
        if param.name in ignored:
            continue

        val = getattr(instance, param.name)
        # Compulsory args-
        if param.default is inspect.Parameter.empty:
            if hasattr(val, "to_dict"):  # convert the user object or any future ones to dict.
                val = val.to_dict()
            json_dict[param.name] = val

        # If we want to test all args (for de_json)-
        # currently not needed, keeping for completeness
        elif param.default is not inspect.Parameter.empty and include_optional_args:
            json_dict[param.name] = val
    return json_dict


def iter_args(instance: ReactionType, de_json_inst: ReactionType, include_optional: bool = False):
    """
    We accept both the regular instance and de_json created instance and iterate over them for
    easy one line testing later one.
    """
    yield instance.type, de_json_inst.type  # yield this here cause it's not available in sig.

    sig = inspect.signature(instance.__class__.__init__)
    for param in sig.parameters.values():
        if param.name in ignored:
            continue
        inst_at, json_at = getattr(instance, param.name), getattr(de_json_inst, param.name)
        if (
            param.default is not inspect.Parameter.empty and include_optional
        ) or param.default is inspect.Parameter.empty:
            yield inst_at, json_at


@pytest.fixture()
def reaction_type(request):
    return request.param()


@pytest.mark.parametrize(
    "reaction_type",
    [
        reaction_type_custom_emoji,
        reaction_type_emoji,
    ],
    indirect=True,
)
class TestReactionTypes:
    def test_slot_behaviour(self, reaction_type):
        inst = reaction_type
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    def test_de_json_required_args(self, bot, reaction_type):
        cls = reaction_type.__class__
        assert cls.de_json(None, bot) is None

        json_dict = make_json_dict(reaction_type)
        const_reaction_type = ReactionType.de_json(json_dict, bot)
        assert const_reaction_type.api_kwargs == {}

        assert isinstance(const_reaction_type, ReactionType)
        assert isinstance(const_reaction_type, cls)
        for reaction_type_at, const_reaction_type_at in iter_args(
            reaction_type, const_reaction_type
        ):
            assert reaction_type_at == const_reaction_type
