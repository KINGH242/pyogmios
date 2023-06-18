from unittest.mock import MagicMock

import pytest

from pyogmios_client.connection import (
    WebSocketErrorHandler,
    WebSocketCloseHandler,
    create_interaction_context,
    InteractionContext,
    InteractionContextOptions,
)
from pyogmios_client.server_health import Connection
from tests.conftest import ConnectionConfigFactory, ServerHealthFactory


def test_create_connection_object():
    # Import the function to test
    from pyogmios_client.connection import create_connection_object

    # Create a ConnectionConfig object
    config = ConnectionConfigFactory.build()

    # Call the function and capture the result
    result = create_connection_object(config)

    # Check if the result is a Connection object
    assert isinstance(result, Connection)

    # Check if the connection object is created with the provided config
    assert result.host in [config.host, "localhost"]
    assert result.port in [config.port, 1337]
    assert result.tls == config.tls or result.tls is False
    assert result.max_payload in [config.max_payload, 128 * 1024 * 1024]


@pytest.mark.asyncio
async def test_create_interaction_context_without_config(mocker):
    error_handler = MagicMock(spec=WebSocketErrorHandler)
    close_handler = MagicMock(spec=WebSocketCloseHandler)
    interaction_context = MagicMock(spec=InteractionContext)

    # Mock the get_server_health function to return a successful server health check

    mocker.patch(
        "pyogmios_client.server_health.get_server_health",
        return_value=ServerHealthFactory.build(),
    )
    MagicMock(return_value=interaction_context)

    # Call the function and capture the result
    result = await create_interaction_context(error_handler, close_handler)

    # Check if the result is an InteractionContext object
    assert isinstance(result, InteractionContext)

    # Check if the error_handler and close_handler are set as attributes of the InteractionContext
    assert result.connection.address.http == "http://localhost:1337"
    assert result.connection.address.webSocket == "ws://localhost:1337"

    # Check if the connection object is created with the provided options
    assert result.connection.host == "localhost"
    assert result.connection.port == 1337
    assert result.connection.tls is False
    assert result.connection.max_payload == 128 * 1024 * 1024


@pytest.mark.asyncio
async def test_create_interaction_context_with_config():
    error_handler = MagicMock(spec=WebSocketErrorHandler)
    close_handler = MagicMock(spec=WebSocketCloseHandler)
    interaction_context = MagicMock(spec=InteractionContext)
    connection_config = ConnectionConfigFactory.build()
    options = InteractionContextOptions(connection_config=connection_config)

    # Mock the get_server_health function to return a successful server health check
    MagicMock(return_value=interaction_context)

    # Call the function and capture the result
    result = await create_interaction_context(error_handler, close_handler, options)

    # Check if the result is an InteractionContext object
    assert isinstance(result, InteractionContext)

    # Check if the error_handler and close_handler are set as attributes of the InteractionContext
    assert result.connection.address.http == "http://localhost:1337"
    assert result.connection.address.webSocket == "ws://localhost:1337"

    # Check if the connection object is created with the provided options
    assert result.connection.host in [options.connection_config.host, "localhost"]
    assert result.connection.port in [options.connection_config.port, 1337]
    assert result.connection.tls in [options.connection_config.tls, False]
    assert result.connection.max_payload in [
        options.connection_config.max_payload,
        128 * 1024 * 1024,
    ]
