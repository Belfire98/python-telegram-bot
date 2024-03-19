ForumTopicEdited
===============

.. autoclass:: telegram.ForumTopicEdited(object)
    :members:
    :special-members: __init__
    :inherited-members:
    :show-inheritance:

    The :class:`ForumTopicEdited` class is a representation of a Telegram Forum Topic that has been edited.

    It is a part of the :mod:`telegram` module and is available since version 20.0.

    Attributes
    ----------
    message_thread_id : int
        Unique identifier for the thread of the message, if the message is not in the primary chat
        thread.

    forum_topic_id : int
        Unique identifier for the forum topic.

    new_title : str or None
        New title of the forum topic, if changed.

    New attributes may be added in the future.

    Methods
    -------
    __init__(self, message_thread_id: int, forum_topic_id: int, new_title: str or None = None)
        Initializes a new ForumTopicEdited object.

    Inherited methods
    -----------------
    from :class:`telegram.TelegramObject`
