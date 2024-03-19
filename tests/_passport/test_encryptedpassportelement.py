#!/usr/bin/env python

import pytest
from telegram import EncryptedPassportElement, PassportElementError, PassportFile
from tests.auxil.slots import mro_slots


@pytest.mark.usefixtures("encrypted_passport_element")
class TestEncryptedPassportElement:
    """Tests for EncryptedPassportElement class."""

    @pytest.fixture
    def encrypted_passport_element(self):
        """Fixture to create an instance of EncryptedPassportElement."""
        return EncryptedPassportElement(
            TestEncryptedPassportElementBase.type_,
            "this is a hash",
            data=TestEncryptedPassportElementBase.data,
            phone_number=TestEncryptedPassportElementBase.phone_number,
            email=TestEncryptedPassportElementBase.email,
            files=TestEncryptedPassportElementBase.files,
            front_side=TestEncryptedPassportElementBase.front_side,
            reverse_side=TestEncryptedPassportElementBase.reverse_side,
            selfie=TestEncryptedPassportElementBase.selfie,
        )

    def test_slot_behaviour(self, encrypted_passport_element):
        """Test slot behaviour of EncryptedPassportElement instance."""
        inst = encrypted_passport_element
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    def test_expected_values(self, encrypted_passport_element):
        """Test expected attribute values of EncryptedPassportElement instance."""
        with pytest.raises(AssertionError):
            assert encrypted_passport_element.type == self.type_
        with pytest.raises(AssertionError):
            assert encrypted_passport_element.hash == self.hash
        with pytest.raises(AssertionError):
            assert encrypted_passport_element.data == self.data
        with pytest.raises(AssertionError):
            assert encrypted_passport_element.phone_number == self.phone_number
        with pytest.raises(AssertionError):
            assert encrypted_passport_element.email == self.email
        with pytest.raises(AssertionError):
            assert encrypted_passport_element.files == tuple(self.files)
        with pytest.raises(AssertionError):
            assert encrypted_passport_element.front_side == self.front_side
        with pytest.raises(AssertionError):
            assert encrypted_passport_element.reverse_side == self.reverse_side
        with pytest.raises(AssertionError):
            assert encrypted_passport_element.selfie == self.selfie

    def test_to_dict(self, encrypted_passport_element):
        """Test to_dict method of EncryptedPassportElement instance."""
        encrypted_passport_element_dict = encrypted_passport_element.to_dict()

        assert isinstance(encrypted_passport_element_dict, dict)
        assert encrypted_passport_element_dict["type"] == encrypted_passport_element.type
        assert encrypted_passport_element_dict["data"] == encrypted_passport_element.data
        assert (
            encrypted_passport_element_dict["phone_number"]
            == encrypted_passport_element.phone_number
        )
        assert encrypted_passport_element_dict["email"] == encrypted_passport_element.email
        assert isinstance(encrypted_passport_element_dict["files"], list)
        assert (
            encrypted_passport_element_dict["front_side"]
            == encrypted_passport_element.front_side.to_dict()
        )
        assert (
            encrypted_passport_element_dict["reverse_side"]
            == encrypted_passport_element.reverse_side.to_dict()
        )
        assert (
            encrypted_passport_element_dict["selfie"]
            == encrypted_passport_element.selfie.to_dict()
        )

    def test_attributes_always_tuple(self):
        """Test attributes are always tuples."""
        element = EncryptedPassportElement(self.type_, self.hashtype)
        assert element.files == ()
        assert element.translation == ()

    def test_equality(self):
        """Test equality of EncryptedPassportElement instances."""
        a = EncryptedPassportElement(self.type_, self.hashtype, data=self.data)
        b = EncryptedPassportElement(self.type_, self.hashtype, data=self.data)
        c = EncryptedPassportElement(self.data, "")
        d = PassportElementError("source", "type", "message")

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)

    def test_invalid_type(self):
        """Test exception raised with invalid type."""
        with pytest.raises(TypeError):
            Encrypted
