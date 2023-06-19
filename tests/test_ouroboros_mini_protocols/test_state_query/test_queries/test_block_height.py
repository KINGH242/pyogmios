from unittest import mock

import pytest

from pyogmios_client.connection import (
    create_interaction_context,
)
from pyogmios_client.models import BlockNoOrOrigin
from pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client import (
    create_state_query_client,
)
from tests.conftest import ServerHealthFactory


@pytest.mark.asyncio
async def test_block_height(mocker):
    mocker.patch(
        "pyogmios_client.server_health.get_server_health",
        return_value=ServerHealthFactory.build(),
    )
    interaction_context = await create_interaction_context()

    with mock.patch("pyogmios_client.utils.socket_utils.ensure_socket_is_open"):
        client = await create_state_query_client(interaction_context)
        block_height = await client.block_height()
        client.shutdown()
        assert isinstance(block_height, BlockNoOrOrigin)
