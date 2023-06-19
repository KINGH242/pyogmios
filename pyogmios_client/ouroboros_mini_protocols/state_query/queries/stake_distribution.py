from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import PoolDistribution
from pyogmios_client.models.response_model import StakeDistributionResponse
from pyogmios_client.models.result_models import EraMismatchResult
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_stake_distribution(response: StakeDistributionResponse) -> bool:
    """
    Check if the response is a stake distribution.
    :param response: The response to check.
    :return: True if the response is a stake distribution, False otherwise.
    """
    return isinstance(response.result, PoolDistribution)


async def stake_distribution(context: InteractionContext) -> PoolDistribution:
    """
    Query the stake distribution.
    :param context: The interaction context to use for the query.
    :return: The stake distribution.
    """
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "stakeDistribution"}
    )

    try:
        response = await query(request_args, context)
        query_response = StakeDistributionResponse(**response.dict())
        result = query_response.result
        if result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("stakeDistribution")
        elif is_stake_distribution(query_response):
            return result
        elif isinstance(result, EraMismatchResult):
            era_mismatch = result.eraMismatch
            raise EraMismatchError(
                str(era_mismatch.queryEra), str(era_mismatch.ledgerEra)
            )
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
