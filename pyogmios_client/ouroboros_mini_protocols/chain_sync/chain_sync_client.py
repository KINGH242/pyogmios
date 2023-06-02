from __future__ import annotations

from typing import List, Callable, Coroutine

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import UnknownResultError
from pyogmios_client.models import (
    RollBackward,
    RollForward,
    PointOrOrigin,
    Any,
    Point,
    Origin,
)
from pyogmios_client.models.base_model import BaseModel
from pyogmios_client.models.response_model import RequestNextResponse
from pyogmios_client.models.result_models import IntersectionFound
from pyogmios_client.ouroboros_mini_protocols.chain_sync.find_intersect import (
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
    roll_backward: Callable[[RollBackward, Callable[[], None]], None]
    roll_forward: Callable[[RollForward, Callable[[], None]], None]


class ChainSyncClient(BaseModel):
    context: InteractionContext
    shutdown: Callable[[], None]
    start_sync: Callable[
        [list[Point | Origin], int], Coroutine[Any, Any, IntersectionFound]
    ]


async def create_chain_sync_client(
    context: InteractionContext,
    message_handlers: ChainSyncMessageHandlers,
    options: Options = None,
) -> ChainSyncClient:
    websocket_app = context.socket

    try:

        def message_handler(response: RequestNextResponse) -> None:
            if response.result.RollBackward:
                message_handlers.roll_backward(
                    response.result.RollBackward, lambda: request_next(websocket_app)
                )
            elif response.result.RollForward:
                message_handlers.roll_forward(
                    response.result.RollForward, lambda: request_next(websocket_app)
                )
            else:
                raise UnknownResultError(response.result)

        def response_handler(response: RequestNextResponse) -> None:
            return (
                Queue().promise_push(message_handler(response))
                if options.sequential is True
                else message_handler(response)
            )

        def on_message(message: str) -> None:
            response = RequestNextResponse.parse_raw(message)
            if response.methodname is MethodName.REQUEST_NEXT:
                try:
                    response_handler(response)
                except Exception as err:
                    print(err)

        websocket_app.on_message = on_message

        def shutdown() -> None:
            try:
                ensure_socket_is_open(websocket_app)
                websocket_app.close()
            except Exception as error:
                print(error)
            else:
                print("Shutting down Chain Sync Client...")

        async def start_sync(
            points: List[PointOrOrigin], in_flight: int
        ) -> IntersectionFound:
            try:
                intersection = await find_intersect(
                    context, points or [create_point_from_current_tip(context)]
                )
                ensure_socket_is_open(websocket_app)
                for _ in range(in_flight or 100):
                    request_next(websocket_app)
            except Exception as error:
                print(error)
            else:
                return intersection

    except Exception:
        pass
    else:
        return ChainSyncClient(
            context=context, shutdown=shutdown, start_sync=start_sync
        )
