import pytest

from pyogmios_client.connection import (
    create_interaction_context,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client import (
    create_state_query_client,
    StateQueryClient,
)


@pytest.mark.asyncio
async def test_create_state_query_client():
    interaction_context = await create_interaction_context()

    client = await create_state_query_client(interaction_context)
    assert isinstance(client, StateQueryClient)
