"""
Module containing the telegram.InlineQueryResultCachedDocument class.
"""

from telegram.inline.inlinequeryresult import InlineQueryResult

class InlineQueryResultCachedDocument(InlineQueryResult):
    """
    Represents a link to a file stored on the Telegram servers.
    By default, this file will be sent by the user with an optional
    caption. Alternatively, you can use input\_message\_content to send
    a message with the specified content instead of the file.

    Attributes:
        id (str): Unique identifier for this result, 1-64 bytes.
        title (str): Title for the result.
        document_url (str): A valid URL for the file.
        mime_type (str): MIME type of the file as determined by the file
            extension.
        description (str): Short description of the result.
        thumb_url (str): URL of the thumbnail for the file.
        thumb_width (int): Thumbnail width.
        thumb_height (int): Thumbnail height.
        reply_markup (telegram.ReplyKeyboardMarkup or telegram.InlineKeyboardMarkup
            or telegram.ForceReply or None): Additional interface options.
            A JSON-serialized object for an inline keyboard,
            custom reply keyboard, or instructions to force a reply from
            the user.
    """
    def __init__(self, id, title, document_url, mime_type, description=None,
                 thumb_url=None, thumb_width=None, thumb_height=None,
                 reply_markup=None):
        super().__init__(id, InlineQueryResult.TYPE_DOCUMENT, title,
                         description, reply_markup)
        self.document_url = document_url
        self.mime_type = mime_type
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def to_dict(self):
        """
        Returns a dictionary representation of the InlineQueryResultCachedDocument
        object
