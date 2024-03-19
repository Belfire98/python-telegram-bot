import pytest
from typing import Any
from unittest.mock import AsyncMock, patch

from telegram import Bot, Credentials, File, PassportData, PassportElementErrorDataField, PassportElementErrorSelfie, PassportFile
from telegram.error import PassportDecryptionError
from tests.auxil.pytest_classes import make_bot
from tests.auxil.slots import mro_slots

RAW_PASSPORT_DATA = {
    # ... (same as before)
}

class TestPassportBase:
    # ... (same as before)

class TestPassportWithoutRequest(TestPassportBase):
    @pytest.mark.parametrize(
        "passport_data,expected_data",
        [
            (PassportData.de_json(RAW_PASSPORT_DATA), RAW_PASSPORT_DATA),
            (
                PassportData.de_json(RAW_PASSPORT_DATA).decrypted_data,
                RAW_PASSPORT_DATA,
            ),
        ],
    )
    def test_de_json_and_to_dict(
        self, passport_data: PassportData, expected_data: dict[str, Any]
    ) -> None:
        assert passport_data.to_dict() == expected_data

    # ... (other test methods remain the same)

@pytest.fixture(scope="module")
def passport_data(bot):
    return PassportData.de_json(RAW_PASSPORT_DATA, bot=bot)

@pytest.mark.asyncio
@patch("telegram.Bot.request", new_callable=AsyncMock)
async def test_mocked_set_passport_data_errors(
    mock_request: AsyncMock, bot: Bot, chat_id: int, passport_data: PassportData
) -> None:
    mock_request.return_value = {
        "ok": True,
        "result": {"message_id": 12345},
    }

    await bot.set_passport_data_errors(
        chat_id,
        [
            PassportElementErrorSelfie(
                "driver_license",
                passport_data.decrypted_credentials.secure_data.driver_license.selfie.file_hash,
                "You're not handsome enough to use this app!",
            ),
            PassportElementErrorDataField(
                "driver_license",
                "expiry_date",
                passport_data.decrypted_credentials.secure_data.driver_license.data.data_hash,
                "Your driver license is expired!",
            ),
        ],
    )

    mock_request.assert_called_once_with(
        "setPassportDataErrors",
        data={
            "user_id": str(chat_id),
            "errors": [
                {
                    "type": "PassportElementErrorSelfie",
                    "subtype": "driver_license",
                    "file_hash": passport_data.decrypted_credentials.secure_data.driver_license.selfie.file_hash,
                    "message": "You're not handsome enough to use this app!",
                },
                {
                    "type": "PassportElementErrorDataField",
                    "subtype": "driver_license",
                    "field_name": "expiry_date",
                    "data_hash": passport_data.decrypted_credentials.secure_data.driver_license.data.data_hash,
                    "message": "Your driver license is expired!",
                },
            ],
        },
    )
