#!/usr/bin/env python

import pytest
from telegram import LabeledPrice, ShippingOption, Voice
from tests.auxil.slots import mro_slots


@pytest.mark.usefixtures("shipping_option")
class TestShippingOption:
    """Tests for the ShippingOption class."""

    id_ = "id"
    title = "title"
    prices = [LabeledPrice("Fish Container", 100), LabeledPrice("Premium Fish Container", 1000)]

    @pytest.mark.parametrize(
        "test_case_id, id_, title, prices",
        [
            ("default", id_, title, prices),
            ("empty_prices", id_, title, []),
            ("different_id", "other_id", title, prices),
            ("different_title", id_, "other_title", prices),
        ],
    )
    def test_expected_values(self, shipping_option, test_case_id, id_, title, prices):
        """Test that the ShippingOption instance has the expected values."""
        shipping_option.id = id_
        shipping_option.title = title
        shipping_option.prices = prices

        assert shipping_option.id == id_
        assert shipping_option.title == title
        assert shipping_option.prices == tuple(prices)

    def test_slot_behaviour(self, shipping_option):
        """Test that the ShippingOption instance behaves correctly with respect to its slots."""
        inst = shipping_option
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    def test_to_dict(self, shipping_option):
        """Test that the ShippingOption instance can be serialized to a dictionary."""
        shipping_option_dict = shipping_option.to_dict()

        assert isinstance(shipping_option_dict, dict)
        assert shipping_option_dict["id"] == shipping_option.id
        assert shipping_option_dict["title"] == shipping_option.title
        assert shipping_option_dict["prices"][0] == shipping_option.prices[0].to_dict()
        assert shipping_option_dict["prices"][1] == shipping_option.prices[1].to_dict()

    @pytest.mark.parametrize(
        "a_id, b_id, a_title, b_title, a_prices, b_prices, id_func",
        [
            (id_, id_, title, title, prices, prices, hash),
            (id_, id_, title, "", prices, [], hash),
            (id_, "other_id", title, title, prices, prices, lambda x: 0),
            (0, id_, title, title, prices, prices, hash),
            (id_, id_, title, title, prices, [], hash),
            (id_, id_, title, title, [], prices, hash),
            (id_, id_, title, title, prices, Voice("someid", "someid", 0).to_dict(), hash),
        ],
    )
    def test_equality(self, shipping_option, a_id, b_id, a_title, b_title, a_prices, b_prices, id_func):
        """Test that the ShippingOption instance is compared correctly with other instances."""
        a = ShippingOption(a_id, a_title, a_prices)
        b = ShippingOption(b_id, b_title, b_prices)

        assert id_func(a) == id_func(b) if a == b else id_func(a) != id_func(b)


@pytest.fixture(scope="module")
def shipping_option():
    return ShippingOption(
        TestShippingOption.id_, TestShippingOption.title, TestShippingOption.prices
   
