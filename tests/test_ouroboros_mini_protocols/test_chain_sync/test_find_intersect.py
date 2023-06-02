from unittest.mock import MagicMock

import pytest

from pyogmios_client.connection import (
    WebSocketErrorHandler,
    WebSocketCloseHandler,
    create_interaction_context,
)
from pyogmios_client.models import Origin
from pyogmios_client.models.result_models import IntersectionFound
from pyogmios_client.ouroboros_mini_protocols.chain_sync.find_intersect import (
    find_intersect,
)


@pytest.mark.asyncio
async def test_find_intersect_success():
    # Arrange
    error_handler = MagicMock(spec=WebSocketErrorHandler)
    close_handler = MagicMock(spec=WebSocketCloseHandler)

    context = await create_interaction_context(error_handler, close_handler)
    points = [Origin()]

    # Act
    result = await find_intersect(context, points)

    # Assert
    assert isinstance(result, IntersectionFound)
