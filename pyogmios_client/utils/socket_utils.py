import asyncio

from websocket import WebSocketApp, getdefaulttimeout

from pyogmios_client.exceptions import WebSocketClosedError


async def ensure_socket_is_open(websocket_app: WebSocketApp) -> None:
    """
    Ensure the socket is open.
    :param websocket_app: The websocket app
    """
    # websocket_app.sock.recv()
    default_timeout = getdefaulttimeout() or 0.1
    while not websocket_app.sock.connected:
        await asyncio.sleep(default_timeout)
    if not websocket_app.sock.connected:
        raise WebSocketClosedError()
