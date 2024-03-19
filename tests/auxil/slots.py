#!/usr/bin/env python

import inspect

def mro_slots(obj, only_parents: bool = False) -> list:
    """
    Returns a list of all slots of a class and its parents.

    Args:
        obj (type): The class or class-instance to get the slots from.
        only_parents (bool, optional): If True, only the slots of the parents are
            returned. Defaults to False.

    Returns:
        list: A list of slot names.

    Raises:
        TypeError: If the object has no __mro__ attribute.
    """
    if not isinstance(obj, type):
        obj = obj.__class__

    classes = (obj.__mro__[1:] if only_parents else obj.__mro__) if hasattr(obj, '__mro__') else []

    if not classes:
        raise TypeError('The object has no __mro__ attribute.')

    return [
        attr
        for cls in classes
        if hasattr(cls, "__slots__") and cls.__slots__ is not None
        for attr in cls.__slots__
    ]
