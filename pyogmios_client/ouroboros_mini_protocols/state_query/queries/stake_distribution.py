from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import EraMismatch, PoolDistribution
from pyogmios_client.models.response_model import StakeDistributionResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_era_mismatch(response: StakeDistributionResponse) -> bool:
    if isinstance(response, EraMismatch):
        return response.eraMismatch is not None


def is_stake_distribution(response: StakeDistributionResponse) -> bool:
    return isinstance(response.result, PoolDistribution)


async def stake_distribution(context: InteractionContext) -> PoolDistribution:
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "stakeDistribution"}
    )

    try:
        response = await query(request_args, context)
        query_response = StakeDistributionResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("stakeDistribution")
        elif is_stake_distribution(query_response):
            return query_response.result
        elif is_era_mismatch(query_response):
            era_mismatch = response.result.eraMismatch
            raise EraMismatchError(
                str(era_mismatch.queryEra), str(era_mismatch.ledgerEra)
            )
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
