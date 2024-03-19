#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2024 Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""This modules contains objects that represents Telegram Replies"""
from typing import Any, Optional, Sequence, Tuple, Union

from telegram._chat import Chat
from telegram._dice import Dice
from telegram._files.animation import Animation
from telegram._files.audio import Audio
from telegram._files.contact import Contact
from telegram._files.document import Document
from telegram._files.location import Location
from telegram._files.photosize import PhotoSize
from telegram._files.sticker import Sticker
from telegram._files.venue import Venue
from telegram._files.video import Video
from telegram._files.videonote import VideoNote
from telegram._files.voice import Voice
from telegram._games.game import Game
from telegram._giveaway import Giveaway, GiveawayWinners
from telegram._linkpreviewoptions import LinkPreviewOptions
from telegram._messageentity import MessageEntity
from telegram._messageorigin import MessageOrigin
from telegram._poll import Poll
from telegram._story import Story
from telegram._telegramobject import TelegramObject
from telegram._utils.argumentparsing import parse_sequence_arg
from telegram._utils.defaultvalue import DEFAULT_NONE
from telegram._utils.types import JSONDict

if TYPE_CHECKING:
    from telegram import Bot


class ExternalReplyInfo(TelegramObject):
    """
    This object contains information about a message that is being replied to, which may
    come from another chat or forum topic.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`origin` is equal.

    .. versionadded:: 20.8

    Args:
        origin (MessageOrigin): Origin of the message replied to by the given
            message.
        chat (Chat, optional): Chat the original message belongs to. Available
            only if the chat is a supergroup or a channel.
        message_id (int, optional): Unique message identifier inside the original chat.
            Available only if the original chat is a supergroup or a channel.
        link_preview_options (LinkPreviewOptions, optional): Options used for
            link preview generation for the original message, if it is a text message
        animation (Animation, optional): Message is an animation, information
            about the animation.
        audio (Audio, optional): Message is an audio file, information about the
            file.
        document (Document, optional): Message is a general file, information
            about the file.
        photo (Sequence[PhotoSize], optional): Message is a photo, available
            sizes of the photo.
        sticker (Sticker, optional): Message is a sticker, information about the
            sticker.
        story (Story, optional): Message is a forwarded story.
        video (Video, optional): Message is a video, information about the video.
        video_note (VideoNote, optional): Message is a video note, information
            about the video message.
        voice (Voice, optional): Message is a voice message, information about
            the file.
        has_media_spoiler (bool, optional): :obj:`True`, if the message media is covered by
            a spoiler animation.
        contact (Contact, optional): Message is a shared contact, information
            about the contact.
        dice (Dice, optional): Message is a dice with random value.
        game (Game, optional): Message is a game, information about the game.
        giveaway (Giveaway, optional): Message is a scheduled giveaway,
            information about the giveaway.
        giveaway_winners (GiveawayWinners, optional): A giveaway with public
            winners was completed.
        invoice (Invoice, optional): Message is an invoice for a payment,
            information about the invoice.
        location (Location, optional): Message is a shared location, information
            about the location.
        poll (Poll, optional): Message is a native poll, information about the
            poll.
        venue (Venue, optional): Message is a venue, information about the venue.

    Attributes:
        origin (MessageOrigin): Origin of the message replied to by the given
            message.
        chat (Chat): Optional. Chat the original message belongs to. Available
            only if the chat is a supergroup or a channel.
        message_id (int): Optional. Unique message identifier inside the original chat.
            Available only if the original chat is a supergroup or a channel.
        link_preview_options (LinkPreviewOptions): Optional. Options used for
            link preview generation for the original message, if it is a text message.
        animation (Animation): Optional. Message is an animation, information
            about the animation.
        audio (Audio): Optional. Message is an audio file, information about the
            file.
        document (Document): Optional. Message is a general file, information
            about the file.
        photo (Tuple
