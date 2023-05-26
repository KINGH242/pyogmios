import asyncio

from pyogmios_client.connection import create_interaction_context, WebSocketErrorHandler, WebSocketCloseHandler


async def main():
    error_handler = WebSocketErrorHandler()
    close_handler = WebSocketCloseHandler()
    context = await create_interaction_context(error_handler, close_handler)
    interaction_context = context.get()
    interaction_context.socket.send("Hello")
    interaction_context.socket.close()
    print(f"InteractionContext: {interaction_context}")

if __name__ == "__main__":
    # asyncio.ensure_future(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())