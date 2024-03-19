#!/usr/bin/env python

import typing as t

from telegram import Update, MessageReactionUpdated, MessageReactionCountUpdated
from telegram._utils.defaultvalue import DEFAULT_TRUE
from telegram._utils.types import RT, SCT, DVType, CCT, HandlerCallback
from telegram.ext._handlers.basehandler import BaseHandler
from telegram.ext._utils._update_parsing import parse_chat_id, parse_username

class MessageReactionHandler(BaseHandler[Update, CCT]):
    """Handler class to handle Telegram updates that contain a message reaction.

    Args:
        callback (HandlerCallback[Update, CCT, RT]): The callback function for this handler.
        chat_id (Optional[SCT[int]]): Filters reactions to allow only those which happen in the
            specified chat ID(s).
        chat_username (Optional[SCT[str]]): Filters reactions to allow only those which happen in
            the specified username(s).
        user_id (Optional[SCT[int]]): Filters reactions to allow only those which are set by the
            specified chat ID(s) (this can be the chat itself in the case of anonymous users,
            see the :paramref:`telegram.MessageReactionUpdated.actor_chat`).
        user_username (Optional[SCT[str]]): Filters reactions to allow only those which are set by
            the specified username(s) (this can be the chat itself in the case of anonymous users,
            see the :paramref:`telegram.MessageReactionUpdated.actor_chat`).
        message_reaction_types (int): Specifies if this handler should handle only updates with
            :attr:`telegram.Update.message_reaction`,
            :attr:`telegram.Update.message_reaction_count` or both.
        block (DVType[bool]): Determines whether the return value of the callback should be
            awaited before processing the next handler in
            :meth:`telegram.ext.Application.process_update`. Defaults to :obj:`True`.

    Attributes:
        callback (HandlerCallback[Update, CCT, RT]): The callback function for this handler.
        message_reaction_types (int): Specifies if this handler should handle only updates with
            :attr:`telegram.Update.message_reaction`,
            :attr:`telegram.Update.message_reaction_count` or both.
        block (bool): Determines whether the callback will run in a blocking way.

    """

    MESSAGE_REACTION_UPDATED: Final[int] = -1
    MESSAGE_REACTION_COUNT_UPDATED: Final[int] = 0
    MESSAGE_REACTION: Final[int] = 1

    def __init__(
        self,
        callback: HandlerCallback[Update, CCT, RT],
        chat_id: t.Optional[SCT[int]] = None,
        chat_username: t.Optional[SCT[str]] = None,
        user_id: t.Optional[SCT[int]] = None,
        user_username: t.Optional[SCT[str]] = None,
        message_reaction_types: int = MESSAGE_REACTION,
        block: DVType[bool] = DEFAULT_TRUE,
    ):
        super().__init__(callback, block=block)
        self.message_reaction_types: int = message_reaction_types

        self._chat_ids = parse_chat_id(chat_id)
        self._chat_usernames = parse_username(chat_username)
        if (user_id or user_username) and message_reaction_types in (
            self.MESSAGE_REACTION,
            self.MESSAGE_REACTION_COUNT_UPDATED,
        ):
            raise ValueError(
                "You can not filter for users and include anonymous reactions. Set "
                "`message_reaction_types` to MESSAGE_REACTION_UPDATED."
            )
        self._user_ids = parse_chat_id(user_id)
        self._user_usernames = parse_username(user_username)

    def check_update(self, update: object) -> bool:
        """Determines whether an update should be passed to this handler's :attr:`callback`.

        Args:
            update (Update | object): Incoming update.

        Returns:
            bool

        """
        if not isinstance(update, Update):
            return False

        if not (
            isinstance(update.message_reaction, MessageReactionUpdated)
            or isinstance(update.message_reaction_count, MessageReactionCountUpdated)
        ):
            return False

        if (
            self.message_reaction_types == self.MESSAGE_REACTION_UPDATED
            and isinstance(update.message_reaction_count, MessageReactionCountUpdated)
        ):
            return False

        if (
            self.message_reaction_types == self.MESSAGE_REACTION_COUNT_UPDATED
            and isinstance(update.message_reaction, MessageReactionUpdated)
        ):
            return False

        if not any((self._chat_ids, self._chat_usernames, self._user_ids, self._user_usernames)):
            return True

        # Extract chat and user IDs and usernames from the update for comparison
        chat_id = chat.id if (chat := update.effective_chat) else None
        chat_username = chat.username if chat else None
        user_id = user.id if (user := update.effective_user) else None
        user_username = user.username if user else None

        return (
            bool(self._chat_ids and (chat_id in self._chat_ids))
            or bool(self._chat_usernames and (chat_username in self._chat_usernames))
            or bool(self._user_ids and (user_id in self._user_ids))
            or bool(self._user_usernames and (user_username in
