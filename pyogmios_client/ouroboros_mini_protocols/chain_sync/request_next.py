from typing import Optional, TypeVar

from websocket import WebSocketApp

from pyogmios_client.enums import MethodName
from pyogmios_client.models.base_model import BaseModel
from pyogmios_client.models.request_model import Request

T = TypeVar("T")


class Options(BaseModel):
    mirror: Optional[dict[str, T]]


def request_next(socket: WebSocketApp, options: Options = None) -> None:
    request = Request.from_base_request(
        method_name=MethodName.REQUEST_NEXT, mirror=options.mirror
    )
    socket.send(request.json())
