#!/usr/bin/env python

from typing import Optional, Sequence, Tuple, TYPE_CHECKING, Union

from telegram._inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram._inline.inlinequeryresult import InlineQueryResult
from telegram._messageentity import MessageEntity
from telegram._utils.argumentparsing import parse_sequence_arg
from telegram._utils.defaultvalue import DEFAULT_NONE
from telegram._utils.types import JSONDict, ODVInput
from telegram.constants import InlineQueryResultType
from telegram.inputmessagecontent import InputMessageContent

if TYPE_CHECKING:
    from telegram import InputMessageContent

class InlineQueryResultGif(InlineQueryResult):
    """
    Represents a link to an animated GIF file. By default, this animated GIF file will be sent by
    the user with optional caption. Alternatively, you can use :attr:`input_message_content` to
    send a message with the specified content instead of the animation.

    Args:
        id (str): Unique identifier for this result,
            :tg-const:`telegram.InlineQueryResult.MIN_ID_LENGTH`-
            :tg-const:`telegram.InlineQueryResult.MAX_ID_LENGTH` Bytes.
        gif_url (str): A valid URL for the GIF file. File size must not exceed 1MB.
        gif_width (Optional[int], optional): Width of the GIF.
        gif_height (Optional[int], optional): Height of the GIF.
        gif_duration (Optional[int], optional): Duration of the GIF in seconds.
        thumbnail_url (str, optional): URL of the static (JPEG or GIF) or animated (MPEG4)
            thumbnail for the result.

            Warning:
                The Bot API does **not** define this as an optional argument. It is formally
                optional for backwards compatibility with the deprecated :paramref:`thumb_url`.
                If you pass neither :paramref:`thumbnail_url` nor :paramref:`thumb_url`,
                :class:`ValueError` will be raised.

            .. versionadded:: 20.2
        thumbnail_mime_type (Optional[str], optional): MIME type of the thumbnail, must be one of
            ``'image/jpeg'``, ``'image/gif'``, or ``'video/mp4'``. Defaults to ``'image/jpeg'``.

            .. versionadded:: 20.2
        title (Optional[str], optional): Title for the result.
        caption (Optional[str], optional): Caption of the GIF file to be sent,
            0-:tg-const:`telegram.constants.MessageLimit.CAPTION_LENGTH` characters
            after entities parsing.
        parse_mode (Union[str, None], optional): |parse_mode|
        caption_entities (Sequence[:class:`telegram.MessageEntity`], optional): |caption_entities|

            .. versionchanged:: 20.0
                |sequenceclassargs|

        reply_markup (:class:`telegram.InlineKeyboardMarkup`, optional): Inline keyboard attached
            to the message.
        input_message_content (:class:`telegram.InputMessageContent`, optional): Content of the
            message to be sent instead of the GIF animation.

    Raises:
        :class:`ValueError`: If neither :paramref:`thumbnail_url` nor :paramref:`thumb_url` is
            supplied or if both are supplied and are not equal.

    Attributes:
        type (:obj:`str`): :tg-const:`telegram.constants.InlineQueryResultType.GIF`.
        id (:obj:`str`): Unique identifier for this result,
            :tg-const:`telegram.InlineQueryResult.MIN_ID_LENGTH`-
            :tg-const:`telegram.InlineQueryResult.MAX_ID_LENGTH` Bytes.
        gif_url (:obj:`str`): A valid URL for the GIF file. File size must not exceed 1MB.
        gif_width (:obj:`int`): Optional. Width of the GIF.
        gif_height (:obj:`int`): Optional. Height of the GIF.
        gif_duration (:obj:`int`): Optional. Duration of the GIF in seconds.
        thumbnail_url (:obj:`str`): URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail
            for the result.

            .. versionadded:: 20.2
        thumbnail_mime_type (:obj:`str`): Optional. MIME type of the thumbnail, must be one of
            ``'image/jpeg'``, ``'image/gif'``, or ``'video/mp4'``. Defaults to ``'image/jpeg'``.

            .. versionadded:: 20.2
        title (:obj:`str`): Optional. Title for the result.
        caption (:obj:`str`): Optional. Caption of the GIF file to be sent,
            0-:tg-const:`telegram.constants.MessageLimit.CAPTION_LENGTH` characters
            after entities parsing.
        parse_mode (:obj:`str`): Optional. |parse_mode|
        caption_entities (Tuple[:class:`telegram.MessageEntity`]): Optional. |captionentitiesattr|

            .. versionchanged:: 20.0

                * |tupleclassattrs|
                * |alwaystuple|
        reply_markup (:class:`telegram.InlineKeyboardMarkup`): Optional
