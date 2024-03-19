#!/usr/bin/env python

import pytest
from unittest import TestCase
from telegram import ShippingAddress, ShippingAddressSlot
from enum import Enum

class ShippingAddressTestSlots(Enum):
    COUNTRY_CODE = "country_code"
    STATE = "state"
    CITY = "city"
    STREET_LINE1 = "street_line1"
    STREET_LINE2 = "street_line2"
    POST_CODE = "post_code"

class TestShippingAddressBase:
    COUNTRY_CODE = "GB"
    STATE = "state"
    CITY = "London"
    STREET_LINE1 = "12 Grimmauld Place"
    STREET_LINE2 = "street_line2"
    POST_CODE = "WC1"

class TestShippingAddress(TestCase, TestShippingAddressBase):
    @pytest.fixture(scope="module")
    def shipping_address(self):
        return ShippingAddress(
            self.COUNTRY_CODE,
            self.STATE,
            self.CITY,
            self.STREET_LINE1,
            self.STREET_LINE2,
            self.POST_CODE,
        )

    def test_slot_behaviour(self, shipping_address):
        inst = shipping_address
        slot_names = set(ShippingAddressTestSlots)
        slot_names.update(vars(inst).keys())
        assert len(slot_names) == len(set(slot_names)), "duplicate slot"
        assert all(getattr(inst, slot) is not None for slot in slot_names), "got extra slot"

    def test_de_json(self):
        json_dict = {
            "country_code": self.COUNTRY_CODE,
            "state": self.STATE,
            "city": self.CITY,
            "street_line1": self.STREET_LINE1,
            "street_line2": self.STREET_LINE2,
            "post_code": self.POST_CODE,
        }
        shipping_address = ShippingAddress.de_json(json_dict)
        assert shipping_address.api_kwargs == {}

        assert shipping_address.country_code == self.COUNTRY_CODE
        assert shipping_address.state == self.STATE
        assert shipping_address.city == self.CITY
        assert shipping_address.street_line1 == self.STREET_LINE1
        assert shipping_address.street_line2 == self.STREET_LINE2
        assert shipping_address.post_code == self.POST_CODE

    def test_to_dict(self, shipping_address):
        shipping_address_dict = shipping_address.to_dict()

        assert isinstance(shipping_address_dict, dict)
        for slot in ShippingAddressTestSlots:
            assert slot.value in shipping_address_dict
            assert shipping_address_dict[slot.value] == getattr(shipping_address, slot.value)

    def test_equality(self):
        a = ShippingAddress(
            self.COUNTRY_CODE,
            self.STATE,
            self.CITY,
            self.STREET_LINE1,
            self.STREET_LINE2,
            self.POST_CODE,
        )
        b = ShippingAddress(
            self.COUNTRY_CODE,
            self.STATE,
            self.CITY,
            self.STREET_LINE1,
            self.STREET_LINE2,
            self.POST_CODE,
        )
        d = ShippingAddress("", self.STATE, self.CITY, self.STREET_LINE1, self.STREET_LINE2, self.POST_CODE)
        d2 = ShippingAddress(
            self.COUNTRY_CODE,
            "",
            self.CITY,
            self.STREET_LINE1,
            self.STREET_LINE2,
            self.POST_CODE,
        )
        d3 = ShippingAddress(
            self.COUNTRY_CODE,
            self.STATE,
            "",
            self.STREET_LINE1,
            self.STREET_LINE2,
            self.POST_CODE,
        )
        d4 = ShippingAddress(
            self.COUNTRY_CODE, self.STATE, self.CITY, "", self.STREET_LINE2, self.POST_CODE
        )
        d5 = ShippingAddress(
            self.COUNTRY_CODE, self.STATE, self.CITY, self.STREET_LINE1, "", self.POST_CODE
        )
        d6 = ShippingAddress(
            self.COUNTRY_CODE, self.STATE, self.CITY, self.STREET_LINE1, self.STREET_LINE2, ""
        )

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a != d
        assert hash(a) != hash(d)

        assert a != d2
        assert hash(a) != hash(d2)

        assert a != d3
        assert hash(a) != hash(d3)

        assert a != d4
        assert hash(a) != hash(d4)

        assert a != d5
        assert hash(a) != hash(d5)

        assert a != d6
        assert hash(a) != hash(d6)
