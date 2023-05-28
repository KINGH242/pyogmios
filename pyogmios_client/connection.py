import threading
from enum import Enum

import websocket
from promise import Promise
from typing import Optional, Callable, Any

from websocket import WebSocketApp

from pyogmios_client.models.base_model import BaseModel
from pyogmios_client.exceptions import ServerNotReady
from pyogmios_client.server_health import (
    get_server_health,
    ConnectionConfig,
    Connection,
)


class InteractionContext(BaseModel):
    connection: Connection
    socket: WebSocketApp
    after_each: Callable[[Any], None]


class InteractionType(Enum):
    OneTime = "OneTime"
    LongRunning = "LongRunning"


class Options(BaseModel):
    connection: Optional[ConnectionConfig]
    interaction_type: Optional[InteractionType]


class WebSocketErrorHandler:
    def __call__(self, ws_app: WebSocketApp, exception: Exception):
        print(exception)


class WebSocketCloseHandler:
    def __call__(self, ws_app: WebSocketApp, close_status_code: int, close_msg: str):
        print(f"Closed with code: {close_status_code} and reason: {close_msg}")


def create_connection_object(config: ConnectionConfig = None) -> Connection:
    host = config.host if config else "localhost"
    port = config.port if config else 1337
    tls = config.tls if config else False
    max_payload = config.max_payload if config else 128 * 1024 * 1024

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
) -> Promise[InteractionContext]:
    connection = create_connection_object(options.connection if options else None)

    health = await get_server_health(
        Options(connection=connection)
    )  # You need to implement this function

    def close_on_completion():
        return (options.interaction_type or "LongRunning") == "OneTime"

    def executor(
        resolve: Callable[[Any], None], reject: Callable[[Exception], None]
    ) -> None:
        if health.last_tip_update is None:
            return reject(ServerNotReady(health))

        def after_each(ws_app: WebSocketApp, callback: callable):
            if close_on_completion():
                ws_app.send("close")
                callback()
                ws_app.close()
            else:
                callback()

        def on_initial_error(ws_app: WebSocketApp, error: Exception):
            ws_app.close()
            return reject(error)

        def on_open(ws_app: WebSocketApp):
            return resolve(
                InteractionContext(
                    connection=connection, socket=ws_app, after_each=after_each
                )
            )

        def on_message(ws_app, message):
            print(f"Message: {message}")
            if message == "error":
                on_initial_error(ws_app, Exception(message))
            elif message == "close":
                return reject(Exception(message))

        websocket.enableTrace(True)
        websocket_app = WebSocketApp(
            connection.address.webSocket,
            on_open=on_open,
            on_close=close_handler,
            on_error=error_handler,
            on_message=on_message,
        )

        websocket_thread = threading.Thread(target=websocket_app.run_forever)
        websocket_thread.daemon = True
        websocket_thread.start()

        return None

    return Promise(executor)
