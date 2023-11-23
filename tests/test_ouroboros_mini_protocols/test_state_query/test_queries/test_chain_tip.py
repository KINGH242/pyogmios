from unittest import mock

import pytest

from pyogmios_client.connection import (
    create_interaction_context,
)
from pyogmios_client.exceptions import QueryUnavailableInCurrentEraError
from pyogmios_client.models import (
    PointOrOrigin,
    Point,
    DigestBlake2bBlockHeader,
    QueryUnavailableInCurrentEra,
)
from pyogmios_client.models.response_model import QueryResponse, QueryResponseReflection
from pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client import (
    create_state_query_client,
)


@pytest.mark.parametrize(
    "test_input",
    [
        Point(slot=123456789, hash=DigestBlake2bBlockHeader(b"1" * 64)),
        "origin",
    ],
)
@pytest.mark.asyncio
async def test_chain_sync(mocker, test_input):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.chain_tip.query",
        return_value=QueryResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result=test_input,
        ),
    )

    interaction_context = await create_interaction_context()

    client = await create_state_query_client(interaction_context)
    chain_tip = await client.chain_tip()
    await client.shutdown()
    assert isinstance(chain_tip, PointOrOrigin)


@pytest.mark.asyncio
async def test_block_height_query_unavailable(mocker):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.chain_tip.query",
        return_value=QueryResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result="QueryUnavailableInCurrentEra",
        ),
    )

    interaction_context = await create_interaction_context()

    # Act & Assert
    with pytest.raises(QueryUnavailableInCurrentEraError) as exc_info:
        with mock.patch(
            "pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client.ensure_socket_is_open"
        ):
            client = await create_state_query_client(interaction_context)
            chain_tip = await client.chain_tip()
            client.shutdown()
            assert isinstance(chain_tip, QueryUnavailableInCurrentEra)
    assert exc_info.value.query_name == "chainTip"
    assert exc_info.value.message == "QueryUnavailableInCurrentEra. chainTip"
