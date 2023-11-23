from typing import Optional, TypeVar

from websocket import WebSocketApp

from pyogmios_client.models.base_model import BaseModel
from pyogmios_client.models.request_model import RequestNext

T = TypeVar("T")


class Options(BaseModel):
    mirror: Optional[dict[str, T]]


def request_next(socket: WebSocketApp, options: Options = None) -> None:
    """
    Request next.
    :param socket: The websocket
    :param options: The options
    """
    request = RequestNext.from_base(mirror=options.mirror if options else None)
    socket.send(request.model_dump_json())
