async def prepare_message(sender_id: int, recipient_id: int, content: str, *args, **kwargs) -> dict:
    """
    Подготавливает сообщение для отправки.

    :param sender_id: Идентификатор отправителя сообщения.
    :param recipient_id: Идентификатор получателя сообщения.
    :param content: Содержимое сообщения.
    :param args: Дополнительные аргументы (не используются в данной реализации).
    :param kwargs: Дополнительные именованные аргументы (не используются в данной реализации).
    :return: Словарь, представляющий сообщение.
    """
    message = {
        'sender_id': sender_id,
        'recipient_id': recipient_id,
        'content': content,
    }
    return message