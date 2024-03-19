from telegram.ext import ApplicationBuilder

def describe_method(method):
    """Return a docstring for a method including the parameter and return types."""
    args = ', '.join(f'{param.name}: {param.annotation}' for param in method.__annotations__.values())
    return f'{method.__doc__}\n\n:param {method.__name__} {args}: {method.return_annotation}'

ApplicationBuilder.__doc__ = describe_method(ApplicationBuilder.build)

.. autoclass:: telegram.ext.ApplicationBuilder
    :members:
    :special-members: __init__, build
