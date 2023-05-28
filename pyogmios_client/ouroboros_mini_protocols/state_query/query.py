import json
from typing import Any, Optional, TypeVar, Callable, Dict, Coroutine

from nanoid import generate
from promise import Promise
from websocket import WebSocketApp

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums.method_name_enum import MethodName
from pyogmios_client.exceptions import UnknownResultError
from pyogmios_client.models.base_model import BaseModel
from pyogmios_client.models.request_model import Request
from pyogmios_client.models.response_model import Response, QueryResponse
from pyogmios_client.request import send


class RequestArgs(BaseModel):
    method_name: MethodName
    args: Optional[Dict[str, Any]]
    mirror: Optional[Any]


class ResponseArgs(BaseModel):
    handler: Callable[
        [
            QueryResponse,
            Callable[[Optional[Response | Promise[Response]]], None],
            Callable[[Exception], None],
        ],
        None,
    ]


T = TypeVar("T")


async def query(
    request_args: RequestArgs, response: ResponseArgs, context: InteractionContext
) -> Coroutine[Any, Any, Promise[Response]]:
    def ws_callable(websocket: WebSocketApp) -> Promise[Response]:
        def executor(
            resolve: Callable[[Any], None], reject: Callable[[Exception], None]
        ) -> None:
            request_id = generate(size=5)

            def listener(_: WebSocketApp, data: str) -> None:
                query_response = QueryResponse(**json.loads(data))
                if query_response.reflection["request_id"] != request_id:
                    return
                _.on_message = None
                try:
                    response.handler(query_response, resolve, reject)
                except Exception as error:
                    return reject(UnknownResultError(error))

            websocket.on_message = listener
            request = Request.from_base_request(
                method_name=request_args.method_name,
                args=request_args.args,
                mirror={**request_args.mirror, "requestId": str(request_id)},
            )
            websocket.send(request.json())

        return Promise(executor)

    return send(ws_callable, context)
