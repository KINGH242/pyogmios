from unittest import mock
from unittest.mock import MagicMock

import pytest

from pyogmios_client.connection import (
    WebSocketErrorHandler,
    WebSocketCloseHandler,
    create_interaction_context,
)
from pyogmios_client.models import NonMyopicMemberRewards, StakeAddress
from pyogmios_client.ouroboros_mini_protocols.chain_sync.chain_sync_client import (
    ChainSyncMessageHandlers,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client import (
    create_state_query_client,
)
from tests.conftest import ServerHealthFactory


@pytest.mark.asyncio
async def test_non_myopic_member_rewards(mocker):
    error_handler = MagicMock(spec=WebSocketErrorHandler)
    close_handler = MagicMock(spec=WebSocketCloseHandler)
    MagicMock(spec=ChainSyncMessageHandlers)

    # Mock the get_server_health function to return a successful server health check

    mocker.patch(
        "pyogmios_client.server_health.get_server_health",
        return_value=ServerHealthFactory.build(),
    )
    interaction_context = await create_interaction_context(error_handler, close_handler)
    # chain_sync_client = await create_chain_sync_client(context, message_handlers, options)

    with mock.patch("pyogmios_client.utils.socket_utils.ensure_socket_is_open"):
        with mock.patch(
            "pyogmios_client.ouroboros_mini_protocols.chain_sync.request_next"
        ) as request_next_mock:
            request_next_mock.return_value = None
            client = await create_state_query_client(interaction_context)
            addr = StakeAddress(
                __root__="stake1uyc7gl90ufh355m9wfwhgs5dcftxvaxrp3gs9h97f4frssq5zhsq4"
            )
            non_myopic_member_rewards = await client.non_myopic_member_rewards([addr])
            client.shutdown()
            assert isinstance(non_myopic_member_rewards, NonMyopicMemberRewards)
