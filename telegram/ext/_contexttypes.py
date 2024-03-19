#!/usr/bin/env python

class ContextTypes(Generic[CCT, UD, CD, BD]):
    """
    Convenience class to gather customizable types of the :class:`telegram.ext.CallbackContext`
    interface.

    Examples:
        :any:`ContextTypes Bot <examples.contexttypesbot>`

    .. seealso:: :wiki:`Architecture Overview <Architecture>`,
        :wiki:`Storing Bot, User and Chat Related Data <Storing-bot%2C-user-and-chat-related-data>`

    .. versionadded:: 13.6

    Args:
        context (:obj:`type`, optional): Determines the type of the ``context`` argument of all
            (error-)handler callbacks and job callbacks. Must be a subclass of
            :class:`telegram.ext.CallbackContext`. Defaults to
            :class:`telegram.ext.CallbackContext`.
        bot_data (:obj:`type`, optional): Determines the type of
            :attr:`context.bot_data <CallbackContext.bot_data>` of all (error-)handler callbacks
            and job callbacks. Defaults to :obj:`dict`.
        chat_data (:obj:`type`, optional): Determines the type of
            :attr:`context.chat_data <CallbackContext.chat_data>` of all (error-)handler callbacks
            and job callbacks. Defaults to :obj:`dict`.
        user_data (:obj:`type`, optional): Determines the type of
            :attr:`context.user_data <CallbackContext.user_data>` of all (error-)handler callbacks
            and job callbacks. Defaults to :obj:`dict`.

    """

    DEFAULT_TYPE: Type[CallbackContext[ExtBot[None], ADict, ADict, ADict]] = CallbackContext
    """Shortcut for the type annotation for the ``context`` argument that's correct for the
    default settings, i.e. if :class:`telegram.ext.ContextTypes` is not used.

    Example:
        .. code:: python

            async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
                ...

    .. versionadded: 20.0
    """

    __slots__ = ("_bot_data", "_chat_data", "_context", "_user_data")

    def __init__(
        self,
        context: Type[CallbackContext[ExtBot[Any], BD, CD, UD]] = CallbackContext,
        bot_data: Type[BD] = dict,
        chat_data: Type[CD] = dict,
        user_data: Type[UD] = dict,
    ):
        if not issubclass(context, CallbackContext):
            raise ValueError("context must be a subclass of CallbackContext.")

        self._context = context
        self._bot_data = bot_data
        self._chat_data = chat_data
        self._user_data = user_data

    @property
    def context(self) -> Type[CCT]:
        """The type of the ``context`` argument of all (error-)handler callbacks and job
        callbacks.
        """
        return self._context  # type: ignore[return-value]

    @property
    def bot_data(self) -> Type[BD]:
        """The type of :attr:`context.bot_data <CallbackContext.bot_data>` of all (error-)handler
        callbacks and job callbacks.
        """
        return self._bot_data  # type: ignore[return-value]

    @property
    def chat_data(self) -> Type[CD]:
        """The type of :attr:`context.chat_data <CallbackContext.chat_data>` of all (error-)handler
        callbacks and job callbacks.
        """
        return self._chat_data  # type: ignore[return-value]

    @property
    def user_data(self) -> Type[UD]:
        """The type of :attr:`context.user_data <CallbackContext.user_data>` of all (error-)handler
        callbacks and job callbacks.
        """
        return self._user_data  # type: ignore[return-value]
