import pytest

from pyogmios_client.connection import (
    create_interaction_context,
)
from pyogmios_client.exceptions import UnknownResultError
from pyogmios_client.models import Bound, RelativeTime, Epoch
from pyogmios_client.models.response_model import (
    EraStartResponse,
    QueryResponseReflection,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client import (
    create_state_query_client,
)


@pytest.mark.asyncio
async def test_era_start(mocker):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.era_start.query",
        return_value=EraStartResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result=Bound(
                time=RelativeTime(123456789), slot=123456789, epoch=Epoch(500)
            ),
        ),
    )

    interaction_context = await create_interaction_context()

    client = await create_state_query_client(interaction_context)
    era_start = await client.era_start()
    assert isinstance(era_start, Bound)


@pytest.mark.asyncio
async def test_era_start_unknown_result(mocker):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.era_start.query",
        return_value=EraStartResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id")
        ),
    )

    # Act & Assert
    with pytest.raises(UnknownResultError) as exc_info:
        interaction_context = await create_interaction_context()
        client = await create_state_query_client(interaction_context)
        era_start = await client.era_start()
        client.shutdown()

        assert isinstance(era_start, EraStartResponse)
        assert exc_info.value.result == era_start
        assert exc_info.value.message == f"Unknown result error:  {era_start}"
