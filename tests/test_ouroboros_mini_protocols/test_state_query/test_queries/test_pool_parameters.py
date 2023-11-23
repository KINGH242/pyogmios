from typing import Dict

import pytest

from pyogmios_client.connection import (
    create_interaction_context,
)
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
)
from pyogmios_client.models import (
    PoolId,
    PoolParameters,
    QueryUnavailableInCurrentEra,
    EraMismatch,
    Era,
)
from pyogmios_client.models.response_model import (
    PoolParametersResponse,
    QueryResponseReflection,
)
from pyogmios_client.models.result_models import EraMismatchResult
from pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client import (
    create_state_query_client,
)
from tests.conftest import PoolParametersFactory


@pytest.mark.asyncio
async def test_pool_parameters(mocker):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.pool_parameters.query",
        return_value=PoolParametersResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result={
                "pool1qqqqqdk4zhsjuxxd8jyvwncf5eucfskz0xjjj64fdmlgj735lr9": PoolParametersFactory.build()
            },
        ),
    )

    interaction_context = await create_interaction_context()
    client = await create_state_query_client(interaction_context)
    pool_parameters = await client.pool_parameters(
        [PoolId("pool1qqqqqdk4zhsjuxxd8jyvwncf5eucfskz0xjjj64fdmlgj735lr9")]
    )
    await client.shutdown()
    assert isinstance(pool_parameters, Dict)
    assert isinstance(list(pool_parameters.values())[0], PoolParameters)


@pytest.mark.asyncio
async def test_pool_parameters_query_unavailable(mocker):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.pool_parameters.query",
        return_value=PoolParametersResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result="QueryUnavailableInCurrentEra",
        ),
    )

    # Act & Assert
    with pytest.raises(QueryUnavailableInCurrentEraError) as exc_info:
        interaction_context = await create_interaction_context()
        client = await create_state_query_client(interaction_context)
        pool_parameters = await client.pool_parameters(
            [PoolId("pool1qqqqqdk4zhsjuxxd8jyvwncf5eucfskz0xjjj64fdmlgj735lr9")]
        )
        client.shutdown()
        assert isinstance(pool_parameters, QueryUnavailableInCurrentEra)
    assert exc_info.value.query_name == "poolParameters"
    assert exc_info.value.message == "QueryUnavailableInCurrentEra. poolParameters"


@pytest.mark.asyncio
async def test_pool_parameters_era_mismatch(mocker, fake_era_mismatch_result):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.pool_parameters.query",
        return_value=PoolParametersResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result=EraMismatch(**fake_era_mismatch_result["eraMismatch"]),
        ),
    )

    # Act & Assert
    with pytest.raises(EraMismatchError) as exc_info:
        interaction_context = await create_interaction_context()
        client = await create_state_query_client(interaction_context)
        pool_parameters = await client.pool_parameters(
            [PoolId("pool1qqqqqdk4zhsjuxxd8jyvwncf5eucfskz0xjjj64fdmlgj735lr9")]
        )
        client.shutdown()
        assert isinstance(pool_parameters, EraMismatchResult)

    query_era = Era(fake_era_mismatch_result["eraMismatch"]["queryEra"]).value
    ledger_era = Era(fake_era_mismatch_result["eraMismatch"]["ledgerEra"]).value

    assert exc_info.value.query_era == query_era
    assert exc_info.value.ledger_era == ledger_era
    assert (
        exc_info.value.message
        == f"Era mismatch. Query from era {query_era}. Ledger is in {ledger_era}"
    )
