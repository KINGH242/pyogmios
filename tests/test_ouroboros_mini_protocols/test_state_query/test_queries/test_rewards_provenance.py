import pytest

from pyogmios_client.connection import (
    create_interaction_context,
)
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
)
from pyogmios_client.models import (
    RewardsProvenance,
    QueryUnavailableInCurrentEra,
    EraMismatch,
    Era,
)
from pyogmios_client.models.response_model import (
    RewardsProvenanceResponse,
    QueryResponseReflection,
)
from pyogmios_client.models.result_models import EraMismatchResult
from pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client import (
    create_state_query_client,
)
from tests.conftest import RewardsProvenanceFactory


@pytest.mark.asyncio
async def test_rewards_provenance(mocker):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.rewards_provenance.query",
        return_value=RewardsProvenanceResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result=RewardsProvenanceFactory.build(),
        ),
    )
    interaction_context = await create_interaction_context()
    client = await create_state_query_client(interaction_context)
    rewards_provenance = await client.rewards_provenance()
    await client.shutdown()
    assert isinstance(rewards_provenance, RewardsProvenance)


@pytest.mark.asyncio
async def test_rewards_provenance_query_unavailable(mocker):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.rewards_provenance.query",
        return_value=RewardsProvenanceResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result="QueryUnavailableInCurrentEra",
        ),
    )

    # Act & Assert
    with pytest.raises(QueryUnavailableInCurrentEraError) as exc_info:
        interaction_context = await create_interaction_context()
        client = await create_state_query_client(interaction_context)
        rewards_provenance = await client.rewards_provenance()
        client.shutdown()
        assert isinstance(rewards_provenance, QueryUnavailableInCurrentEra)
    assert exc_info.value.query_name == "rewardsProvenance"
    assert exc_info.value.message == "QueryUnavailableInCurrentEra. rewardsProvenance"


@pytest.mark.asyncio
async def test_rewards_provenance_era_mismatch(mocker, fake_era_mismatch_result):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.queries.rewards_provenance.query",
        return_value=RewardsProvenanceResponse.from_base_response(
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result=EraMismatch(**fake_era_mismatch_result["eraMismatch"]),
        ),
    )

    # Act & Assert
    with pytest.raises(EraMismatchError) as exc_info:
        interaction_context = await create_interaction_context()
        client = await create_state_query_client(interaction_context)
        rewards_provenance = await client.rewards_provenance()
        client.shutdown()
        assert isinstance(rewards_provenance, EraMismatchResult)

    query_era = Era(fake_era_mismatch_result["eraMismatch"]["queryEra"]).value
    ledger_era = Era(fake_era_mismatch_result["eraMismatch"]["ledgerEra"]).value

    assert exc_info.value.query_era == query_era
    assert exc_info.value.ledger_era == ledger_era
    assert (
        exc_info.value.message
        == f"Era mismatch. Query from era {query_era}. Ledger is in {ledger_era}"
    )
