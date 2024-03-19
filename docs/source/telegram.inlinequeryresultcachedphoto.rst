"""
Module containing the InlineQueryResultCachedPhoto class.

This class represents a result of an inline query that is a photo that is already
stored in Telegram's cloud storage.
"""

from telegram.inline.inlinequeryresult import InlineQueryResult

class InlineQueryResultCachedPhoto(InlineQueryResult):
    """
    Represents a result of an inline query that is a photo that is already
    stored in Telegram's cloud storage.

    For more information, see
    https://core.telegram.org/bots/api#inlinequeryresultcachedphoto

    :param id: Unique identifier for this result, 1-64 bytes.
    :type id: str
    :param photo_file_id: A valid file identifier for the photo.
    :type photo_file_id: str
    :param title: Title for the result.
    :type title: str
    :param description: Short description of the result.
    :type description: str
    :param caption: Caption of the photo to be displayed in the message.
    :type caption: str, optional
    :param parse_mode: Send Markdown or HTML, if you want Telegram apps to show
                       bold, italic, fixed-width text or inline URLs in the media
                       caption.
    :type parse_mode: str, optional
    :param caption_entities: List of special entities that appear in the caption,
                             which can be specified instead of parse\_mode.
    :type caption_entities: List of MessageEntity, optional
    :param reply_markup: Additional interface options. A JSON-serialized object
                         for an inline keyboard, custom reply keyboard,
                         instructions to remove keyboard or to force a reply from
                         the user.
    :type reply_markup: InlineKeyboardMarkup, KeyboardButton, KeyboardButtonPollType,
                         ReplyKeyboardRemove or ForceReply, optional
    """

    def __init__(self, id, photo_file_id, title, description, caption=None,
                 parse_mode=None, caption
