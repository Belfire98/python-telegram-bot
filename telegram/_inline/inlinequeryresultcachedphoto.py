#!/usr/bin/env python

from typing import Literal, Optional, Sequence, Tuple, Union

from telegram._inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram._inline.inlinequeryresult import InlineQueryResult
from telegram._messageentity import MessageEntity
from telegram._utils.argumentparsing import parse_sequence_arg
from telegram._utils.defaultvalue import DEFAULT_NONE
from telegram._utils.types import JSONDict, ODVInput, Serializable

if TYPE_CHECKING:
    from telegram import InputMessageContent, InputMessageContentABC

class InlineQueryResultCachedPhoto(InlineQueryResult, Serializable):
    """
    Represents a link to a photo stored on the Telegram servers. By default, this photo will be
    sent by the user with an optional caption. Alternatively, you can use
    :attr:`input_message_content` to send a message with the specified content instead
    of the photo.

    .. seealso:: :wiki:`Working with Files and Media <Working-with-Files-and-Media>`

    Args:
        type (Literal['photo']): Type of the result, must be :tg-const:`telegram.constants.InlineQueryResultType.PHOTO`.
        id (str): Unique identifier for this result,
            :tg-const:`telegram.InlineQueryResult.MIN_ID_LENGTH`-
            :tg-const:`telegram.InlineQueryResult.MAX_ID_LENGTH` Bytes.
        photo_file_id (str): A valid file identifier of the photo.
        title (Optional[str]): Title for the result.
        description (Optional[str]): Short description of the result.
        caption (Optional[str]): Caption of the photo to be sent,
            0-:tg-const:`telegram.constants.MessageLimit.CAPTION_LENGTH` characters after
            entities parsing.
        parse_mode (Union[str, None]): |parse_mode|
        caption_entities (Sequence[:class:`telegram.MessageEntity`]): |caption_entities|

            .. versionchanged:: 20.0
                |sequenceclassargs|

        reply_markup (Optional[:class:`telegram.InlineKeyboardMarkup`]): Inline keyboard attached
            to the message.
        input_message_content (Optional[:class:`telegram.InputMessageContent`]): Content of the
            message to be sent instead of the photo.

    Attributes:
        type (Literal['photo']): Type of the result, must be :tg-const:`telegram.constants.InlineQueryResultType.PHOTO`.
        id (str): Unique identifier for this result,
            :tg-const:`telegram.InlineQueryResult.MIN_ID_LENGTH`-
            :tg-const:`telegram.InlineQueryResult.MAX_ID_LENGTH` Bytes.
        photo_file_id (str): A valid file identifier of the photo.
        title (Optional[str]): Optional. Title for the result.
        description (Optional[str]): Optional. Short description of the result.
        caption (Optional[str]): Optional. Caption of the photo to be sent,
            0-:tg-const:`telegram.constants.MessageLimit.CAPTION_LENGTH` characters after
            entities parsing.
        parse_mode (Union[str, None]): Optional. |parse_mode|
        caption_entities (Tuple[:class:`telegram.MessageEntity`]): Optional. |captionentitiesattr|

            .. versionchanged:: 20.0

                * |tupleclassattrs|
                * |alwaystuple|
        reply_markup (Optional[:class:`telegram.InlineKeyboardMarkup`]): Optional. Inline keyboard
            attached to the message.
        input_message_content (Optional[:class:`telegram.InputMessageContent`]): Optional. Content
            of the message to be sent instead of the photo.

    """

    __slots__ = (
        "caption",
        "caption_entities",
        "description",
        "id",
        "input_message_content",
        "parse_mode",
        "photo_file_id",
        "reply_markup",
        "title",
    )

    def __init__(
        self,
        *,
        type: Literal['photo'] = InlineQueryResultType.PHOTO,
        id: str,
        photo_file_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        caption: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[InputMessageContent] = None,
        parse_mode: ODVInput[str] = DEFAULT_NONE,
        caption_entities: Optional[Sequence[MessageEntity]] = None,
        **kwargs,
    ):
        super().__init__(type=type, id=id, **kwargs)
        self.photo_file_id: str = photo_file_id
        self.title: Optional[str] = title
        self.description: Optional[str] = description
        self.caption: Optional[str] = caption
        self.parse_mode: ODVInput[str] = parse_mode
        self.caption_entities: Tuple[MessageEntity, ...] = parse_sequence_arg(caption_entities)
        self.reply_markup: Optional[InlineKeyboardMarkup] = reply_markup
        self.input_message_content: Optional[InputMessageContent] = input_message_content

    @classmethod
    def from_dict(cls, data: JSONDict) -> "InlineQueryResultCachedPhoto":
        data = data.copy()
        data.pop("type")
        return super().from_dict(data
