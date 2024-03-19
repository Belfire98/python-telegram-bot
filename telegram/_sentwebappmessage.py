#!/usr/bin/env python

class SentWebAppMessage(TelegramObject):
    """Information about an inline message sent by a Web App on behalf of a user.

    This class is comparable in terms of equality. Two instances are considered equal if their
    `inline_message_id` attributes are equal.

    Attributes:
        inline_message_id (Optional[str]): Identifier of the sent inline message. Available only if
            there is an inline keyboard attached to the message.

    Args:
        inline_message_id (Optional[str], optional): Identifier of the sent inline message.
            Available only if there is an inline keyboard attached to the message.

    Raises:
        ValueError: If `inline_message_id` is not a string.

    Examples:
        >>> message = SentWebAppMessage(inline_message_id="some_id")
        >>> message.inline_message_id
        'some_id'
        >>> message == SentWebAppMessage(inline_message_id="some_id")
        True
        >>> message == SentWebAppMessage(inline_message_id="other_id")
        False
    """

    __slots__ = ("inline_message_id",)

    def __init__(self, inline_message_id: Optional[str] = None):
        if inline_message_id is not None and not isinstance(inline_message_id, str):
            raise ValueError("`inline_message_id` must be a string")

        super().__init__()
        self.inline_message_id = inline_message_id

        self._id_attrs = (self.inline_message_id,)

        self._freeze()
