from websocket import WebSocketApp

from pyogmios_client.exceptions import WebSocketClosedError


async def ensure_socket_is_open(websocket_app: WebSocketApp) -> None:
    """
    Ensure the socket is open.
    :param websocket_app: The websocket app
    """
    if not websocket_app.sock.connected:
        raise WebSocketClosedError()
