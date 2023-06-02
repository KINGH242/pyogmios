from unittest.mock import MagicMock

import pytest

from pyogmios_client.connection import (
    WebSocketErrorHandler,
    WebSocketCloseHandler,
    create_interaction_context,
)
from pyogmios_client.models.response_model import Response
from pyogmios_client.ouroboros_mini_protocols.state_query.query import query
from tests.conftest import RequestArgsFactory


@pytest.mark.asyncio
async def test_query_success():
    # Arrange
    error_handler = MagicMock(spec=WebSocketErrorHandler)
    close_handler = MagicMock(spec=WebSocketCloseHandler)
    request_args = RequestArgsFactory.build()
    context = await create_interaction_context(error_handler, close_handler)

    # Act
    result = await query(request_args, context)

    # Assert
    print(f"Result: {result}")
    assert isinstance(result, Response)


@pytest.mark.asyncio
async def test_query_error(mock_to_send):
    # Arrange
    error_handler = MagicMock(spec=WebSocketErrorHandler)
    close_handler = MagicMock(spec=WebSocketCloseHandler)
    request_args = RequestArgsFactory.build()
    context = await create_interaction_context(error_handler, close_handler)

    # Act
    result = await query(request_args, context)

    # Assert
    assert result == "Expected error result"
