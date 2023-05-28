from typing import Callable, TypeVar, Any

from promise import Promise
from websocket import WebSocketApp

from pyogmios_client.connection import InteractionContext

T = TypeVar("T")


async def send(
    ws_app: Callable[[WebSocketApp], Promise[T]], context: InteractionContext
) -> Promise[T]:
    socket = context.socket
    after_each = context.after_each

    def executor(
        resolve: Callable[[Any], None], reject: Callable[[Exception], None]
    ) -> None:
        ws_app(socket).then(lambda result: after_each(resolve(result))).catch(
            lambda error: reject(error)
        )
        return None

    return Promise(executor)
