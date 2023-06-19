from unittest import mock

import pytest

from pyogmios_client.connection import (
    create_interaction_context,
)
from pyogmios_client.models import PointOrOrigin
from pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client import (
    create_state_query_client,
)
from tests.conftest import ServerHealthFactory


@pytest.mark.asyncio
async def test_chain_sync(mocker):
    mocker.patch(
        "pyogmios_client.server_health.get_server_health",
        return_value=ServerHealthFactory.build(),
    )
    interaction_context = await create_interaction_context()

    with mock.patch("pyogmios_client.utils.socket_utils.ensure_socket_is_open"):
        client = await create_state_query_client(interaction_context)
        chain_tip = await client.chain_tip()
        assert isinstance(chain_tip, PointOrOrigin)
