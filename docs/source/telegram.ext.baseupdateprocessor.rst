.. currentmodule:: telegram.ext

UpdateProcessor Base Class
=========================

.. autoclass:: BaseUpdateProcessor
    :members: 
    :undoc-members: 
    :show-inheritance:

    This is the base class for all update processors. It handles the basic logic of processing updates and dispatching them to the appropriate handlers.

    Example:
        To create a custom update processor, you can inherit from this class and override the necessary methods:

        ```python
        from telegram.ext import BaseUpdateProcessor, MessageHandler, Filters

        class CustomUpdateProcessor(BaseUpdateProcessor):

            def register_handlers(self, dispatcher):
                self.dispatcher = dispatchler
                self.add_handler(MessageHandler(Filters.text & (~Filters.command), self.on_text_message))

            def on_text_message(self, update, context):
                # Your custom logic here
                pass
        ```
