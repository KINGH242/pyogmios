from typing import Callable, TypeVar

from websocket import WebSocketApp

from pyogmios_client.connection import InteractionContext

T = TypeVar("T")


async def send(to_send: Callable[[WebSocketApp], T], context: InteractionContext) -> T:
    socket = context.socket
    after_each = context.after_each

    try:
        result = await to_send(socket)
    except Exception as error:
        raise error
    else:
        after_each(socket, lambda: print("after_each"))
        return result

    # def executor(
    #     resolve: Callable[[Any], None], reject: Callable[[Exception], None]
    # ) -> None:
    #     ws_app(socket).then(lambda result: after_each(resolve(result))).catch(
    #         lambda error: reject(error)
    #     )
    #     return None

    # return Promise(executor)
