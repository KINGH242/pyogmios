import json
from typing import Any, Optional, TypeVar, Callable, Dict

from nanoid import generate
from websocket import WebSocketApp

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.models.base_model import BaseModel
from pyogmios_client.models.request_model import Request
from pyogmios_client.models.response_model import Response, QueryResponse
from pyogmios_client.request import send

T = TypeVar("T")


class RequestArgs(BaseModel):
    method_name: MethodName
    args: Optional[Dict[str, Any]]
    mirror: Optional[Any]


class ResponseHandlerArgs(BaseModel):
    response: QueryResponse
    resolve: Callable[[Optional[Response]], None]
    reject: Callable[[Exception], None]


class ResponseArgs(BaseModel):
    handler: Callable[[ResponseHandlerArgs], T]


async def query(request_args: RequestArgs, context: InteractionContext) -> Response:
    async def to_send(websocket: WebSocketApp) -> Response | None:
        try:
            request_id = generate(size=5)

            request = Request.from_base_request(
                method_name=request_args.method_name,
                args=request_args.args,
                mirror={**request_args.mirror, "requestId": str(request_id)}
                if request_args.mirror
                else {"requestId": str(request_id)},
            )
            websocket.send(request.json())
            result = websocket.sock.recv()
            query_response = QueryResponse(**json.loads(result))

            if query_response.reflection.requestId != request_id:
                return

            return result
        except Exception as error:
            raise error

    response = await send(to_send, context)
    return Response(**json.loads(response))
    # return send(to_send, context)
