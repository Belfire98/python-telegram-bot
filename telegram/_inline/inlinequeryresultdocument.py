#!/usr/bin/env python
from dataclasses import dataclass
from typing import Literal, NamedTuple, Optional

from telegram._inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram._inline.inlinequeryresult import InlineQueryResult
from telegram._messageentity import MessageEntity
from telegram._utils.argumentparsing import parse_sequence_arg
from telegram._utils.defaultvalue import DEFAULT_NONE
from telegram._utils.types import JSONDict
from telegram.constants import InlineQueryResultType, MessageLimit

@dataclass(slots=True)
class InlineQueryResultDocument(InlineQueryResult):
    """
    Represents a link to a file. By default, this file will be sent by the user with an optional
    caption. Alternatively, you can use :attr:`input_message_content` to send a message with the
    specified content instead of the file. Currently, only .PDF and .ZIP files can be sent
    using this method.

    Args:
        id (str): Unique identifier for this result,
            :tg-const:`telegram.InlineQueryResult.MIN_ID_LENGTH`-
            :tg-const:`telegram.InlineQueryResult.MAX_ID_LENGTH` Bytes.
        type (Literal[InlineQueryResultType.DOCUMENT]): Type of the result.
        title (str): Title for the result.
        caption (Optional[str]): Caption of the document to be sent,
            0-:tg-const:`telegram.constants.MessageLimit.CAPTION_LENGTH` characters
            after entities parsing.
        parse_mode (Optional[str]): |parse_mode|
        caption_entities (Optional[Sequence[:class:`telegram.MessageEntity`]]): |caption_entities|

            .. versionchanged:: 20.0
                |sequenceclassargs|

        document_url (str): A valid URL for the file.
        mime_type (str): Mime type of the content of the file, either "application/pdf"
            or "application/zip".
        description (Optional[str]): Short description of the result.
        reply_markup (Optional[:class:`telegram.InlineKeyboardMarkup`]): Inline keyboard attached
            to the message.
        input_message_content (Optional[:class:`telegram.InputMessageContent`]): Content of the
            message to be sent instead of the file.
        thumbnail_url (Optional[str]): URL of the thumbnail (JPEG only) for the file.

            .. versionadded:: 20.2
        thumbnail_width (Optional[int]): Thumbnail width.

            .. versionadded:: 20.2
        thumbnail_height (Optional[int]): Thumbnail height.

            .. versionadded:: 20.2

    Attributes:
        type (Literal[InlineQueryResultType.DOCUMENT]): Type of the result.
        id (str): Unique identifier for this result,
            :tg-const:`telegram.InlineQueryResult.MIN_ID_LENGTH`-
            :tg-const:`telegram.InlineQueryResult.MAX_ID_LENGTH` Bytes.
        title (str): Title for the result.
        caption (Optional[str]): Caption of the document to be sent,
            0-:tg-const:`telegram.constants.MessageLimit.CAPTION_LENGTH` characters
            after entities parsing.
        parse_mode (Optional[str]): |parse_mode|
        caption_entities (Tuple[:class:`telegram.MessageEntity`]): Optional. |captionentitiesattr|

            .. versionchanged:: 20.0

                * |tupleclassattrs|
                * |alwaystuple|
        document_url (str): A valid URL for the file.
        mime_type (str): Mime type of the content of the file, either "application/pdf"
            or "application/zip".
        description (Optional[str]): Short description of the result.
        reply_markup (Optional[:class:`telegram.InlineKeyboardMarkup`]): Inline keyboard attached
            to the message.
        input_message_content (Optional[:class:`telegram.InputMessageContent`]): Content of the
            message to be sent instead of the file.
        thumbnail_url (Optional[str]): Optional. URL of the thumbnail (JPEG only) for the file.

            .. versionadded:: 20.2
        thumbnail_width (Optional[int]): Optional. Thumbnail width.

            .. versionadded:: 20.2
        thumbnail_height (Optional[int]): Optional. Thumbnail height.

            .. versionadded:: 20.2

    """

    type: Literal[InlineQueryResultType.DOCUMENT]
    id: str
    title: str
    caption: Optional[str]
    parse_mode: Optional[str] = DEFAULT_NONE
    caption_entities: Optional[NamedTuple("CaptionEntities", [("entities", Sequence[MessageEntity])])] = None
    document_url: str
    mime_type: str
    description: Optional[str]
    reply_markup: Optional[InlineKeyboardMarkup]
    input_message_content: Optional["InputMessageContent"]
    thumbnail_url: Optional[str]
    thumbnail_width: Optional[int]
    thumbnail_height: Optional[int]

    def __post_init__(self):
        if self.caption_entities is not None:
            self.caption_entities = parse_sequence_arg(self.caption_entities.entities)

    def to_dict(self):
        result = super().to_dict()
       
