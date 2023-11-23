import pytest

from pyogmios_client.connection import (
    create_interaction_context,
)
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
)
from pyogmios_client.models import Epoch, QueryUnavailableInCurrentEra, Era
from pyogmios_client.models.response_model import QueryResponse, QueryResponseReflection
from pyogmios_client.models.result_models import EraMismatchResult
from pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client import (
    create_state_query_client,
)


@pytest.mark.asyncio
async def test_current_epoch(mocker):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.current_epoch.query",
        return_value=QueryResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result=Epoch(500),
        ),
    )
    interaction_context = await create_interaction_context()

    client = await create_state_query_client(interaction_context)
    current_epoch = await client.current_epoch()
    assert isinstance(current_epoch, Epoch)


@pytest.mark.asyncio
async def test_current_epoch_query_unavailable(mocker):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.current_epoch.query",
        return_value=QueryResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result="QueryUnavailableInCurrentEra",
        ),
    )

    # Act & Assert
    with pytest.raises(QueryUnavailableInCurrentEraError) as exc_info:
        interaction_context = await create_interaction_context()
        client = await create_state_query_client(interaction_context)
        current_epoch = await client.current_epoch()
        assert isinstance(current_epoch, QueryUnavailableInCurrentEra)
    assert exc_info.value.query_name == "currentEpoch"
    assert exc_info.value.message == "QueryUnavailableInCurrentEra. currentEpoch"


@pytest.mark.asyncio
async def test_current_epoch_era_mismatch(mocker, fake_era_mismatch_result):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.current_epoch.query",
        return_value=QueryResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result=EraMismatchResult(**fake_era_mismatch_result),
        ),
    )

    # Act & Assert
    with pytest.raises(EraMismatchError) as exc_info:
        interaction_context = await create_interaction_context()
        client = await create_state_query_client(interaction_context)
        current_epoch = await client.current_epoch()
        assert isinstance(current_epoch, QueryUnavailableInCurrentEra)
    assert exc_info.value.query_era == Era.Byron.value
    assert exc_info.value.ledger_era == Era.Mary.value
    assert (
        exc_info.value.message
        == f"Era mismatch. Query from era {Era.Byron.value}. Ledger is in {Era.Mary.value}"
    )
