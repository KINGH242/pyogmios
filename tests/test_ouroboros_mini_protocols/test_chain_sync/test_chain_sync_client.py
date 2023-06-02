from unittest import mock
from unittest.mock import MagicMock

import pytest

from pyogmios_client.connection import (
    WebSocketErrorHandler,
    WebSocketCloseHandler,
    create_interaction_context,
)
from pyogmios_client.ouroboros_mini_protocols.chain_sync.chain_sync_client import (
    create_chain_sync_client,
    ChainSyncMessageHandlers,
    ChainSyncClient,
)
from tests.conftest import ServerHealthFactory


# @pytest.fixture
# def context():
#     return InteractionContext()
#
#
# @pytest.fixture
# def message_handlers():
#     return ChainSyncMessageHandlers()
#
#
# @pytest.fixture
# def options():
#     return Options(sequential=True)
#
#
# @pytest.fixture
# def response():
#     return RequestNextResponse(methodname=MethodName.REQUEST_NEXT)


@pytest.mark.asyncio
async def test_create_chain_sync_client(mocker):
    error_handler = MagicMock(spec=WebSocketErrorHandler)
    close_handler = MagicMock(spec=WebSocketCloseHandler)
    message_handlers = MagicMock(spec=ChainSyncMessageHandlers)

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
            client = await create_chain_sync_client(
                interaction_context, message_handlers
            )
            assert isinstance(client, ChainSyncClient)
