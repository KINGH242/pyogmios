import json
from typing import Dict
from unittest.mock import MagicMock

import pytest

from pyogmios_client.connection import (
    WebSocketErrorHandler,
    WebSocketCloseHandler,
    create_interaction_context,
)
from pyogmios_client.request import send
from tests.conftest import RequestFactory


@pytest.mark.asyncio
async def test_send():
    error_handler = MagicMock(spec=WebSocketErrorHandler)
    close_handler = MagicMock(spec=WebSocketCloseHandler)

    context = await create_interaction_context(error_handler, close_handler)

    async def to_send(socket) -> Dict:
        request = RequestFactory.build()
        socket.send(request.json())
        response = socket.sock.recv()
        response = json.loads(response)
        print(f"Response: {response}")
        return response

    # Mock the WebSocketApp.send method to be an async function
    # WebSocketApp.send.return_value = asyncio.Future()

    # Call the send function and capture the result
    result = await send(to_send, context)

    # Check if the to_send function is called with the WebSocketApp object
    # to_send.assert_called_with(context.socket)

    # Check if the context.after_each method is called with the WebSocketApp object
    # context.after_each.assert_called_with(context.socket)

    # Check if the result is the return value of the to_send function
    assert isinstance(result, dict)
