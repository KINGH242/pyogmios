from typing import Union
from unittest import mock
from unittest.mock import MagicMock

import pytest

from pyogmios_client.connection import (
    WebSocketErrorHandler,
    WebSocketCloseHandler,
    create_interaction_context,
)
from pyogmios_client.models import (
    ProtocolParametersBabbage,
    ProtocolParametersAlonzo,
    ProtocolParametersShelley,
)
from pyogmios_client.ouroboros_mini_protocols.chain_sync.chain_sync_client import (
    ChainSyncMessageHandlers,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client import (
    create_state_query_client,
)
from tests.conftest import ServerHealthFactory


@pytest.mark.asyncio
async def test_current_protocol_parameters(mocker):
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
            current_protocol_parameters = await client.current_protocol_parameters()
            assert isinstance(
                current_protocol_parameters,
                Union[
                    ProtocolParametersBabbage,
                    ProtocolParametersAlonzo,
                    ProtocolParametersShelley,
                ],
            )
