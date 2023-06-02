import threading
from enum import Enum

import websocket
from typing import Optional, Callable

from websocket import WebSocketApp

from pyogmios_client.models.base_model import BaseModel
from pyogmios_client.exceptions import ServerNotReady, WebSocketClosedError
from pyogmios_client.server_health import (
    get_server_health,
    ConnectionConfig,
    Connection,
    Options as ServerHealthOptions,
)


class InteractionContext(BaseModel):
    connection: Connection
    socket: WebSocketApp
    after_each: Callable[[WebSocketApp, Callable[[], None]], None]


class InteractionType(Enum):
    OneTime = "OneTime"
    LongRunning = "LongRunning"


class Options(BaseModel):
    connection_config: Optional[ConnectionConfig]
    interaction_type: Optional[InteractionType]


class WebSocketErrorHandler:
    def __call__(self, ws_app: WebSocketApp, exception: Exception):
        print(exception)


class WebSocketCloseHandler:
    def __call__(self, ws_app: WebSocketApp, close_status_code: int, close_msg: str):
        print(f"Closed with code: {close_status_code} and reason: {close_msg}")


def create_connection_object(config: ConnectionConfig = None) -> Connection:
    host = config.host or "localhost" if config else "localhost"
    port = config.port or 1337 if config else 1337
    tls = config.tls or False if config else False
    max_payload = (
        config.max_payload or 128 * 1024 * 1024 if config else 128 * 1024 * 1024
    )

    host_and_port = f"{host}:{port}"

    connection = {
        "host": host,
        "port": port,
        "tls": tls,
        "max_payload": max_payload,
        "address": {
            "http": f"https://{host_and_port}" if tls else f"http://{host_and_port}",
            "webSocket": f"wss://{host_and_port}" if tls else f"ws://{host_and_port}",
        },
    }
    return Connection(**connection)


async def create_interaction_context(
    error_handler: WebSocketErrorHandler,
    close_handler: WebSocketCloseHandler,
    options: Options = None,
) -> InteractionContext | None:
    connection = create_connection_object(
        options.connection_config if options else None
    )

    health = await get_server_health(
        ServerHealthOptions(connection=connection)
    )  # You need to implement this function

    def close_on_completion():
        return (
            (options.interaction_type or "LongRunning") == "OneTime"
            if options
            else "OneTime"
        )

    try:
        if health.last_tip_update is None:
            raise ServerNotReady(health)

        def after_each(ws_app: WebSocketApp, callback: Callable[[], None]):
            if close_on_completion():
                ws_app.send("close")
                callback()
                ws_app.close()
            else:
                callback()

        def on_initial_error(ws_app: WebSocketApp, error: Exception):
            ws_app.close()
            raise error

        def on_open(ws_app: WebSocketApp):
            return InteractionContext(
                connection=connection, socket=ws_app, after_each=after_each
            )

        def on_message(ws_app, message):
            print(f"Message: {message}")
            if message == "error":
                on_initial_error(ws_app, Exception(message))
            elif message == "close":
                raise WebSocketClosedError()

        websocket.enableTrace(True)
        websocket_app = WebSocketApp(
            connection.address.webSocket,
            on_open=on_open,
            on_message=on_message,
            on_close=close_handler,
            on_error=error_handler,
        )

        websocket_thread = threading.Thread(target=websocket_app.run_forever)
        websocket_thread.daemon = True
        websocket_thread.start()

    except ServerNotReady as e:
        print(e)
        return None
    else:
        return InteractionContext(
            connection=connection, socket=websocket_app, after_each=after_each
        )
