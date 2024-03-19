from telegram.inline.inlinequeryresult import InlineQueryResult
from telegram.sticker import Sticker
from telegram.utils.helpers import mention_html

class InlineQueryResultCachedSticker(InlineQueryResult):
    """
    Represents a link to a sticker file stored on the Telegram servers. By default, this
    sticker will be sent by the user with optional inline keyboard attached.
    The bot can also modify the way it is sent using the :class:`telegram.InputMediaSticker`
    class.

    Objects of this class are comparable in terms of their :attr:`id` attributes.

    Args:
        id (str): Unique identifier for this result, 1-64 Bytes.
        sticker_file_id (str): A valid file_id of the sticker as defined by
            `Telegram Bot API <https://core.telegram.org/bots/api#file>`_.
        title (str, optional): Title for the result.
        description (str, optional): Short description of the result.
        caption (str, optional): Caption of the sticker, 0-200 characters.
        parse_mode (str, optional): Mode for parsing entities in the caption.
            See :class:`telegram.ParseMode` for more details.
        reply_markup (:class:`telegram.KeyboardMarkup` or :class:`telegram.InlineKeyboardMarkup`, optional):
            The object representing the inline keyboard that should be
            sent along with the message.
        input_message_content (:class:`telegram.InputMessageContent`, optional):
            Content of the message to be sent instead of the sticker.

    Attributes:
        id (str): Unique identifier for this result, 1-64 Bytes.
        sticker_file_id (str): A valid file_id of the sticker as defined by
            `Telegram Bot API <https://core.telegram.org/bots/api#file>`_.
        title (str, optional): Title for the result.
        description (str, optional): Short description of the result.
        caption (
