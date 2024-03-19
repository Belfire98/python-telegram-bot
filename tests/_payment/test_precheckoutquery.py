#!/usr/bin/env python

import pytest
from typing import Any, Dict, Optional

from telegram import Bot, OrderInfo, PreCheckoutQuery, Update, User
from telegram.bot import Bot as BotType
from telegram.error import TelegramError
from tests.auxil.bot_method_checks import (
    check_defaults_handling,
    check_shortcut_call,
    check_shortcut_signature,
)
from tests.auxil.slots import mro_slots


@pytest.fixture(scope="module")
def pre_checkout_query(bot: BotType) -> PreCheckoutQuery:
    pcq = PreCheckoutQuery(
        TestPreCheckoutQueryBase.id_,
        TestPreCheckoutQueryBase.from_user,
        TestPreCheckoutQueryBase.currency,
        TestPreCheckoutQueryBase.total_amount,
        TestPreCheckoutQueryBase.invoice_payload,
        shipping_option_id=TestPreCheckoutQueryBase.shipping_option_id,
        order_info=TestPreCheckoutQueryBase.order_info,
    )
    pcq.set_bot(bot)
    return pcq


class TestPreCheckoutQueryBase:
    id_: int = 5
    invoice_payload: str = "invoice_payload"
    shipping_option_id: str = "shipping_option_id"
    currency: str = "EUR"
    total_amount: int = 100
    from_user: User = User(0, "", False)
    order_info: OrderInfo = OrderInfo()


def test_slot_behaviour(pre_checkout_query: PreCheckoutQuery) -> None:
    inst = pre_checkout_query
    for attr in inst.__slots__:
        assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
    assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"


def test_de_json(bot: BotType) -> None:
    json_dict: Dict[str, Any] = {
        "id": TestPreCheckoutQueryBase.id_,
        "invoice_payload": TestPreCheckoutQueryBase.invoice_payload,
        "shipping_option_id": TestPreCheckoutQueryBase.shipping_option_id,
        "currency": TestPreCheckoutQueryBase.currency,
        "total_amount": TestPreCheckoutQueryBase.total_amount,
        "from": TestPreCheckoutQueryBase.from_user.to_dict(),
        "order_info": TestPreCheckoutQueryBase.order_info.to_dict(),
    }
    pre_checkout_query = PreCheckoutQuery.de_json(json_dict, bot)
    assert pre_checkout_query.api_kwargs == {}

    assert pre_checkout_query.get_bot() is bot
    assert pre_checkout_query.id == TestPreCheckoutQueryBase.id_
    assert pre_checkout_query.invoice_payload == TestPreCheckoutQueryBase.invoice_payload
    assert pre_checkout_query.shipping_option_id == TestPreCheckoutQueryBase.shipping_option_id
    assert pre_checkout_query.currency == TestPreCheckoutQueryBase.currency
    assert pre_checkout_query.from_user == TestPreCheckoutQueryBase.from_user
    assert pre_checkout_query.order_info == TestPreCheckoutQueryBase.order_info


def test_to_dict(pre_checkout_query: PreCheckoutQuery) -> None:
    pre_checkout_query_dict: Dict[str, Any] = pre_checkout_query.to_dict()

    assert isinstance(pre_checkout_query_dict, dict)
    assert pre_checkout_query_dict["id"] == pre_checkout_query.id
    assert pre_checkout_query_dict["invoice_payload"] == pre_checkout_query.invoice_payload
    assert (
        pre_checkout_query_dict["shipping_option_id"] == pre_checkout_query.shipping_option_id
    )
    assert pre_checkout_query_dict["currency"] == pre_checkout_query.currency
    assert pre_checkout_query_dict["from"] == pre_checkout_query.from_user.to_dict()
    assert pre_checkout_query_dict["order_info"] == pre_checkout_query.order_info.to_dict()


def test_equality() -> None:
    a = PreCheckoutQuery(
        TestPreCheckoutQueryBase.id_,
        TestPreCheckoutQueryBase.from_user,
        TestPreCheckoutQueryBase.currency,
        TestPreCheckoutQueryBase.total_amount,
        TestPreCheckoutQueryBase.invoice_payload,
    )
    b = PreCheckoutQuery(
        TestPreCheckoutQueryBase.id_,
        TestPreCheckoutQueryBase.from_user,
        TestPreCheckoutQueryBase.currency,
        TestPreCheckoutQueryBase.total_amount,
        TestPreCheckoutQueryBase.invoice_payload,
    )
    c = PreCheckoutQuery(TestPreCheckoutQueryBase.id_, None, "", 0, "")
    d = PreCheckoutQuery(0, TestPreCheckoutQueryBase.from_user, TestPreCheckoutQueryBase.currency,
