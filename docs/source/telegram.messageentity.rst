.. currentmodule:: telegram

.. autoclass:: MessageEntity
    :members:
    :special-members: __init__
    :undoc-members:
    :show-inheritance:

    The :class:`MessageEntity` class is used to represent various entities found within a message,
    such as URLs, usernames, hashtags, etc.

    Attributes:
        type (str): The type of the entity, one of "mention", "hashtag", "cashtag", "bot_command",
            "url", "email", "phone_number", "bold", "italic", "underline", "strikethrough",
            "spoiler", "code", "pre", "text_link", "text_mention" or "custom_emoji".
        offset (int): The offset of the entity in the message text.
        length (int): The length of the entity in the message text.
        url (str, optional): The URL of the entity, if applicable.
        user (:class:`User`, optional): The user to which the entity refers, if applicable.
        language (str, optional): The language of the entity, if applicable.
        custom_emoji_id (str, optional): The ID of the custom emoji, if applicable.
        entities (List[:class:`MessageEntity`], optional): A list of nested entities, if applicable.
