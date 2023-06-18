import logging
from typing import Callable, TypeVar

from websocket import WebSocketApp

from pyogmios_client.connection import InteractionContext

T = TypeVar("T")


async def send(to_send: Callable[[WebSocketApp], T], context: InteractionContext) -> T:
    """
    Sends a request to the node.
    :param to_send: The function to send the request.
    :param context: The interaction context to use for the request.
    :return: The response.
    """
    socket = context.socket
    after_each = context.after_each

    try:
        result = await to_send(socket)
    except Exception as error:
        raise error
    else:
        after_each(socket, lambda: logging.debug(result))
        return result
