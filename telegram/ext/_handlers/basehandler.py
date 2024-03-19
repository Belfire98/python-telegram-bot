#!/usr/bin/env python

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

import telegram
from telegram._utils.defaultvalue import DEFAULT_TRUE
from telegram._utils.repr import build_repr_with_selected_attrs
from telegram._utils.types import DVType
from telegram.ext._utils.types import CCT, HandlerCallback

if TYPE_CHECKING:
    from telegram.ext import Application

RT = TypeVar("RT")
UT = TypeVar("UT")


class BaseHandler(Generic[UT, CCT], ABC):
    """The base class for all update handlers. Create custom handlers by inheriting from it.

    Warning:
        When setting :paramref:`block` to :obj:`False`, you cannot rely on adding custom
        attributes to :class:`telegram.ext.CallbackContext`. See its docs for more info.

    This class is a :class:`~typing.Generic` class and accepts two type variables:

    1. The type of the updates that this handler will handle. Must coincide with the type of the
       first argument of :paramref:`callback`. :meth:`check_update` must only accept
       updates of this type.
    2. The type of the second argument of :paramref:`callback`. Must coincide with the type of the
       parameters :paramref:`handle_update.context` and
       :paramref:`collect_additional_context.context` as well as the second argument of
       :paramref:`callback`. Must be either :class:`~telegram.ext.CallbackContext` or a subclass
       of that class.

       .. tip::
           For this type variable, one should usually provide a :class:`~typing.TypeVar` that is
           also used for the mentioned method arguments. That way, a type checker can check whether
           this handler fits the definition of the :class:`~Application`.

    .. seealso:: :wiki:`Types of Handlers <Types-of-Handlers>`

    .. versionchanged:: 20.0

        * The attribute ``run_async`` is now :paramref:`block`.
        * This class was previously named ``Handler``.

    Attributes:
        callback (:term:`coroutine function`): The callback function for this handler.
        block (:obj:`bool`): Determines whether the callback will run in a blocking way.

    """

    __slots__ = (
        "block",
        "callback",
    )

    def __init__(
        self,
        callback: HandlerCallback[UT, CCT, RT],
        block: DVType[bool] = DEFAULT_TRUE,
    ):
        self.callback: HandlerCallback[UT, CCT, RT] = callback
        self.block: DVType[bool] = block

    def __repr__(self) -> str:
        """Give a string representation of the handler in the form ``ClassName[callback=...]``.

        As this class doesn't implement :meth:`object.__str__`, the default implementation
        will be used, which is equivalent to :meth:`__repr__`.

        Returns:
            :obj:`str`
        """
        try:
            callback_name = self.callback.__qualname__
        except AttributeError:
            callback_name = repr(self.callback)
        return build_repr_with_selected_attrs(self, callback=callback_name)

    @abstractmethod
    def check_update(self, update: object) -> Optional[Union[bool, object]]:
        """
        This method is called to determine if an update should be handled by
        this handler instance. It should always be overridden.

        Note:
            Custom updates types can be handled by the application. Therefore, an implementation of
            this method should always check the type of :paramref:`update`.

        Args:
            update (:obj:`object` | :class:`telegram.Update`): The update to be tested.

        Returns:
            Either :obj:`None` or :obj:`False` if the update should not be handled. Otherwise an
            object that will be passed to :meth:`handle_update` and
            :meth:`collect_additional_context` when the update gets handled.

        """

    async def handle_update(
        self,
        update: UT,
        application: "Application[Any, CCT, Any, Any, Any, Any
