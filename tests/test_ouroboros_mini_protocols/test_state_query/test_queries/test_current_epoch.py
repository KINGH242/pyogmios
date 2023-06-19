from unittest import mock

import pytest

from pyogmios_client.connection import (
    create_interaction_context,
)
from pyogmios_client.models import Epoch
from pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client import (
    create_state_query_client,
)


@pytest.mark.asyncio
async def test_current_epoch():
    interaction_context = await create_interaction_context()

    with mock.patch("pyogmios_client.utils.socket_utils.ensure_socket_is_open"):
        client = await create_state_query_client(interaction_context)
        current_epoch = await client.current_epoch()
        assert isinstance(current_epoch, Epoch)
