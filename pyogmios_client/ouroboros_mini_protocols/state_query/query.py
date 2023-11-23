from typing import Any, Optional, TypeVar, Callable, Dict

from nanoid import generate
from websocket import WebSocketApp

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.models.base_model import BaseModel
from pyogmios_client.models.request_model import Request
from pyogmios_client.models.response_model import Response, QueryResponse
from pyogmios_client.request import send, send_request

T = TypeVar("T")


class RequestArgs(BaseModel):
    method_name: MethodName
    args: Optional[Dict[str, Any]] = None
    mirror: Optional[Any] = None


class ResponseHandlerArgs(BaseModel):
    response: QueryResponse
    resolve: Callable[[Optional[Response]], None]
    reject: Callable[[Exception], None]


class ResponseArgs(BaseModel):
    handler: Callable[[ResponseHandlerArgs], T]


async def query(
    request_args: RequestArgs, context: InteractionContext
) -> QueryResponse | None:
    """
    Sends a query to the node.
    :param request_args: The request arguments.
    :param context: The interaction context to use for the query.
    :return: The query response.
    """

    async def to_send(_: WebSocketApp) -> QueryResponse | None:
        """
        Sends the query to the node.
        :param _: The websocket to use for the query.
        :return: The query response.
        """
        try:
            request_id = generate(size=5)

            if request_args.mirror:
                if "requestId" in request_args.mirror:
                    request_id = request_args.mirror["requestId"]
                    mirror = request_args.mirror
                elif isinstance(request_args.mirror, dict):
                    mirror = {**request_args.mirror, "requestId": request_id}
                elif isinstance(request_args.mirror, list):
                    mirror = {*request_args.mirror, {"requestId": request_id}}
                else:
                    mirror = {"mirror": request_args.mirror, "requestId": request_id}
            else:
                mirror = {"requestId": request_id}

            request = Request.from_base_request(
                method_name=request_args.method_name,
                args=request_args.args,
                mirror=mirror,
            )

            raw_response = await send_request(request, context)
            query_response = QueryResponse.model_validate(raw_response.model_dump())

            if query_response.reflection.requestId != request_id:
                return

            return query_response
        except Exception as error:
            raise error

    return await send(to_send, context)
