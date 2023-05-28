from __future__ import annotations

from typing import List, Optional, Callable, Any

from promise import Promise

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums.method_name_enum import MethodName
from pyogmios_client.exceptions import UnknownResultError
from pyogmios_client.models import RollBackward, RollForward
from pyogmios_client.models.base_model import BaseModel
from pyogmios_client.models.point_model import PointOrOrigin
from pyogmios_client.models.response_model import RequestNextResponse
from pyogmios_client.ouroboros_mini_protocols.chain_sync.find_intersect import (
    Intersection,
    find_intersect,
    create_point_from_current_tip,
)
from pyogmios_client.ouroboros_mini_protocols.chain_sync.request_next import (
    request_next,
)
from pyogmios_client.utils.queue import Queue
from pyogmios_client.utils.socket_utils import ensure_socket_is_open


class Options(BaseModel):
    sequential: bool


class ChainSyncMessageHandlers(BaseModel):
    roll_backward: Callable[[RollBackward, Callable[[], None]], Promise[None]]
    roll_forward: Callable[[RollForward, Callable[[], None]], Promise[None]]


class ChainSyncClient(BaseModel):
    context: InteractionContext
    shutdown: Callable[[], Promise[None]]
    start_sync: Callable[
        [Optional[List[PointOrOrigin]], int], Promise[Optional[Intersection]]
    ]


async def create_chain_sync_client(
    context: InteractionContext,
    message_handlers: ChainSyncMessageHandlers,
    options: Options = None,
) -> Promise[ChainSyncClient]:
    websocket_app = context.socket

    def executor(
        resolve: Callable[[Any], None], _: Callable[[Exception], None]
    ) -> None:
        def message_handler(response: RequestNextResponse) -> None:
            if response.result.roll_backward:
                await message_handlers.roll_backward(
                    response.result.RollBackward, lambda: request_next(websocket_app)
                )
            elif response.result.roll_forward:
                await message_handlers.roll_forward(
                    response.result.RollForward, lambda: request_next(websocket_app)
                )
            else:
                raise UnknownResultError(response.result)

        def response_handler(response: RequestNextResponse) -> Promise[None]:
            return (
                Queue().promise_push(message_handler(response))
                if options.sequential is True
                else message_handler(response)
            )

        def on_message(message: str) -> None:
            response = RequestNextResponse.parse_raw(message)
            if response.method_name is MethodName.REQUEST_NEXT:
                try:
                    await response_handler(response)
                except Exception as error:
                    print(error)

        websocket_app.on_message = on_message

        def shutdown() -> Promise[None]:
            def shutdown_executor(
                res: Callable[[Any], None], rej: Callable[[Exception], None]
            ) -> None:
                ensure_socket_is_open(websocket_app)
                websocket_app.on_close = res
                websocket_app.close()

            return Promise(shutdown_executor)

        def start_sync(
            points: List[PointOrOrigin], in_flight: int
        ) -> Promise[Intersection]:
            def start_sync_executor(
                res: Callable[[Any], None], rej: Callable[[Exception], None]
            ) -> None:
                intersection = await find_intersect(
                    context, points or [create_point_from_current_tip(context)]
                )
                ensure_socket_is_open(websocket_app)
                for _ in range(in_flight or 100):
                    request_next(websocket_app)
                return res(intersection)

            return Promise(start_sync_executor)

        return resolve(
            ChainSyncClient(context=context, shutdown=shutdown, start_sync=start_sync)
        )

    return Promise(executor)
