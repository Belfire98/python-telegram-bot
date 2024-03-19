#!/usr/bin/env python

import pytest
from telegram.errors import PassportElementErrorFile, PassportElementErrorSelfie
from tests.auxil.slots import mro_slots


@pytest.fixture(scope="module")
def passport_element_error_file():
    return PassportElementErrorFile(
        TestPassportElementErrorFileBase.type_,
        TestPassportElementErrorFileBase.file_hash,
        TestPassportElementErrorFileBase.message,
    )


class TestPassportElementErrorFileBase:
    source: str = "file"
    type_: str = "test_type"
    file_hash: str = "file_hash"
    message: str = "Error message"


class TestPassportElementErrorFileWithoutRequest(TestPassportElementErrorFileBase):
    def test_slot_behaviour(self, passport_element_error_file: PassportElementErrorFile) -> None:
        """Test slot behaviour of PassportElementErrorFile instance."""
        inst = passport_element_error_file
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(mro_slots(inst)) == len(set(mro_slots(inst))), "duplicate slot"

    def test_expected_values(self, passport_element_error_file: PassportElementErrorFile) -> None:
        """Test expected values of PassportElementErrorFile instance."""
        assert passport_element_error_file.source == self.source
        assert passport_element_error_file.type == self.type_
        assert passport_element_error_file.file_hash == self.file_hash
        assert passport_element_error_file.message == self.message

    def test_to_dict(self, passport_element_error_file: PassportElementErrorFile) -> None:
        """Test to_dict method of PassportElementErrorFile instance."""
        passport_element_error_file_dict = passport_element_error_file.to_dict()

        assert isinstance(passport_element_error_file_dict, dict)
        assert passport_element_error_file_dict["source"] == passport_element_error_file.source
        assert passport_element_error_file_dict["type"] == passport_element_error_file.type
        assert passport_element_error_file_dict["file_hash"] == passport_element_error_file.file_hash
        assert passport_element_error_file_dict["message"] == passport_element_error_file.message

    def test_equality(self) -> None:
        """Test equality of PassportElementErrorFile instances."""
        a = PassportElementErrorFile(self.type_, self.file_hash, self.message)
        b = PassportElementErrorFile(self.type_, self.file_hash, self.message)
        c = PassportElementErrorFile(self.type_, "", "")
        d = PassportElementErrorFile("", self.file_hash, "")
        e = PassportElementErrorFile("", "", self.message)
        f = PassportElementErrorSelfie(self.type_, self.file_hash, self.message)

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a != c
        assert hash(a) != hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)

        assert a != f
        assert hash(a) != hash(f)
