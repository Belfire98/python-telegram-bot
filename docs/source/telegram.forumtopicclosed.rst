ForumTopicClosed
===============

.. autoclass:: telegram.ForumTopicClosed(
    :noindex:
    :members: 
    :inherited-members:
    :special-members: __init__
    :undoc-members:
    :show-inheritance:
)

This class represents a closed forum topic in Telegram.

It is a subclass of :class:`telegram.ForumTopic`, and has the following attributes:

- **message_thread_id** (:class:`int`): The ID of the message thread that contains this forum topic.
- **closed_by** (:class:`telegram.User`): The user who closed this forum topic.
- **closed_at** (:class:`datetime.datetime`): The date and time when this forum topic was closed.

Example usage:

.. code-block:: python

    from telegram import ForumTopicClosed

    topic = ForumTopicClosed(
        message_thread_id=12345,
        closed_by=User(id=67890, is_bot=False, first_name='Alice'),
        closed_at=datetime.datetime.utcnow()
    )

    print(topic.closed_by.first_name)  # Output: Alice
    print(topic.closed_at)  # Output: The date and time when the topic was closed
