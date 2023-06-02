import asyncio

from pyogmios_client.connection import (
    create_interaction_context,
    WebSocketErrorHandler,
    WebSocketCloseHandler,
)


async def main():
    error_handler = WebSocketErrorHandler()
    close_handler = WebSocketCloseHandler()
    context = await create_interaction_context(error_handler, close_handler)
    context.socket.send("Hello")
    context.socket.close()
    print(f"InteractionContext: {context}")


if __name__ == "__main__":
    # asyncio.ensure_future(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
