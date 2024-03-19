#!/usr/bin/env python

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from telegram._payment.orderinfo import OrderInfo
from telegram._telegramobject import TelegramObject
from telegram._utils.types import JSONDict

if TYPE_CHECKING:
    from telegram import Bot

class SuccessfulPayment(TelegramObject):
    """This object contains basic information about a successful payment.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`telegram_payment_charge_id` and
    :attr:`provider_payment_charge_id` are equal.

    Args:
        currency (str): Three-letter ISO 4217 currency code.
        total_amount (int): Total price in the smallest units of the currency (integer, not
            float/double). For example, for a price of US$ 1.45 pass ``amount = 145``.
            See the ``exp`` parameter in
            `currencies.json <https://core.telegram.org/bots/payments/currencies.json>`_,
            it shows the number of digits past the decimal point for each currency
            (2 for the majority of currencies).
        invoice_payload (str): Bot specified invoice payload.
        shipping_option_id (Optional[str], optional): Identifier of the shipping option chosen by the
            user.
        order_info (Optional[OrderInfo], optional): Order info provided by the user.
        telegram_payment_charge_id (str): Telegram payment identifier.
        provider_payment_charge_id (str): Provider payment identifier.

    Attributes:
        currency (str): Three-letter ISO 4217 currency code.
        total_amount (int): Total price in the smallest units of the currency (integer, not
            float/double). For example, for a price of US$ 1.45 ``amount`` is ``145``.
            See the ``exp`` parameter in
            `currencies.json <https://core.telegram.org/bots/payments/currencies.json>`_,
            it shows the number of digits past the decimal point for each currency
            (2 for the majority of currencies).
        invoice_payload (str): Bot specified invoice payload.
        shipping_option_id (Optional[str]): Identifier of the shipping option chosen by the
            user.
        order_info (Optional[OrderInfo]): Order info provided by the user.
        telegram_payment_charge_id (str): Telegram payment identifier.
        provider_payment_charge_id (str): Provider payment identifier.

    """

    __slots__ = (
        "currency",
        "invoice_payload",
        "order_info",
        "provider_payment_charge_id",
        "shipping_option_id",
        "telegram_payment_charge_id",
        "total_amount",
    )

    def __init__(
        self,
        currency: str,
        total_amount: int,
        invoice_payload: str,
        telegram_payment_charge_id: str,
        provider_payment_charge_id: str,
        shipping_option_id: Optional[str] = None,
        order_info: Optional[OrderInfo] = None,
        **api_kwargs: JSONDict,
    ):
        super().__init__(api_kwargs=api_kwargs)
        self.currency: str = currency
        self.total_amount: int = total_amount
        self.invoice_payload: str = invoice_payload
        self.shipping_option_id: Optional[str] = shipping_option_id
        self.order_info: Optional[OrderInfo] = order_info
        self.telegram_payment_charge_id: str = telegram_payment_charge_id
        self.provider_payment_charge_id: str = provider_payment_charge_id

        self._id_attrs = (self.telegram_payment_charge_id, self.provider_payment_charge_id)

        self._freeze()

    @classmethod
    def from_dict(cls, data: Dict[str, Any], bot: Bot) -> Optional["SuccessfulPayment"]:
        """Create a SuccessfulPayment instance from a dictionary."""
        data = cls._parse_data(data)

        if not data:
            return None

        data["order_info"] = OrderInfo.de_json(data.get("order_info"), bot)

        return super().from_dict(data=data, bot=bot)

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: Bot) -> Optional["SuccessfulPayment"]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        return cls.from_dict(json.loads(data), bot)
