from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import PoolsRanking
from pyogmios_client.models.response_model import PoolsRankingResponse
from pyogmios_client.models.result_models import EraMismatchResult
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_pools_ranking(response: PoolsRankingResponse) -> bool:
    """
    Check if the response is a list of pool ids.
    :param response: The response to check.
    :return: True if the response is a list of pool ids, False otherwise.
    """
    result = response.result
    if isinstance(result, PoolsRanking):
        return True
    return False


async def pools_ranking(context: InteractionContext) -> PoolsRanking:
    """
    Query the pools ranking.
    :param context: The interaction context to use for the query.
    :return: The pools ranking.
    """
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "poolsRanking"}
    )

    try:
        response = await query(request_args, context)
        query_response = PoolsRankingResponse(**response.dict())
        result = query_response.result
        if result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("poolsRanking")
        elif isinstance(result, EraMismatchResult):
            era_mismatch = result.eraMismatch
            raise EraMismatchError(
                str(era_mismatch.queryEra), str(era_mismatch.ledgerEra)
            )
        elif is_pools_ranking(query_response):
            return query_response.result
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
