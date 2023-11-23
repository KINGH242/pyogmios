import pytest

from pyogmios_client.connection import (
    create_interaction_context,
)
from pyogmios_client.exceptions import QueryUnavailableInCurrentEraError
from pyogmios_client.models import BlockNoOrOrigin, QueryUnavailableInCurrentEra
from pyogmios_client.models.response_model import QueryResponse, QueryResponseReflection
from pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client import (
    create_state_query_client,
)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (BlockNoOrOrigin(123456789), BlockNoOrOrigin),
        ("origin", BlockNoOrOrigin),
    ],
)
@pytest.mark.asyncio
async def test_block_height(mocker, test_input, expected):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.block_height.query",
        return_value=QueryResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result=test_input,
        ),
    )

    interaction_context = await create_interaction_context()

    client = await create_state_query_client(interaction_context)
    block_height = await client.block_height()
    await client.shutdown()
    assert isinstance(block_height, expected)


@pytest.mark.asyncio
async def test_block_height_query_unavailable(mocker):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.block_height.query",
        return_value=QueryResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result="QueryUnavailableInCurrentEra",
        ),
    )

    interaction_context = await create_interaction_context()

    # Act & Assert
    with pytest.raises(QueryUnavailableInCurrentEraError) as exc_info:
        client = await create_state_query_client(interaction_context)
        block_height = await client.block_height()
        client.shutdown()
        assert isinstance(block_height, QueryUnavailableInCurrentEra)
    assert exc_info.value.query_name == "blockHeight"
    assert exc_info.value.message == "QueryUnavailableInCurrentEra. blockHeight"
