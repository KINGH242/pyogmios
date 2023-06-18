from unittest import mock
from unittest.mock import MagicMock

import pytest

from pyogmios_client.connection import (
    create_interaction_context,
)
from pyogmios_client.ouroboros_mini_protocols.chain_sync.chain_sync_client import (
    ChainSyncMessageHandlers,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client import (
    create_state_query_client,
    StateQueryClient,
)
from tests.conftest import ServerHealthFactory


@pytest.mark.asyncio
async def test_create_state_query_client(mocker):
    message_handlers = MagicMock(spec=ChainSyncMessageHandlers)
    MagicMock(spec=ChainSyncMessageHandlers)

    # Mock the get_server_health function to return a successful server health check

    mocker.patch(
        "pyogmios_client.server_health.get_server_health",
        return_value=ServerHealthFactory.build(),
    )
    interaction_context = await create_interaction_context(message_handlers)
    # chain_sync_client = await create_chain_sync_client(context, message_handlers, options)

    with mock.patch("pyogmios_client.utils.socket_utils.ensure_socket_is_open"):
        with mock.patch(
            "pyogmios_client.ouroboros_mini_protocols.chain_sync.request_next"
        ) as request_next_mock:
            request_next_mock.return_value = None
            client = await create_state_query_client(interaction_context)
            assert isinstance(client, StateQueryClient)
