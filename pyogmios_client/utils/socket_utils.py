from websocket import WebSocketApp

from pyogmios_client.exceptions import WebSocketClosedError


def ensure_socket_is_open(websocket_app: WebSocketApp) -> None:
    websocket_app.sock.recv()
    if not websocket_app.sock.connected:
        raise WebSocketClosedError()
