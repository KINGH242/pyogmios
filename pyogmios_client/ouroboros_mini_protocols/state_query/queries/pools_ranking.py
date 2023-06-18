from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import EraMismatch, PoolsRanking
from pyogmios_client.models.response_model import PoolsRankingResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_era_mismatch(response: PoolsRankingResponse) -> bool:
    if isinstance(response, EraMismatch):
        return response.eraMismatch is not None


def is_pools_ranking(response: PoolsRankingResponse) -> bool:
    result = response.result
    if isinstance(result, PoolsRanking):
        return True
    return False


async def pools_ranking(context: InteractionContext) -> PoolsRanking:
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "poolsRanking"}
    )

    try:
        response = await query(request_args, context)
        query_response = PoolsRankingResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("poolsRanking")
        elif is_era_mismatch(query_response):
            era_mismatch = response.result.eraMismatch
            raise EraMismatchError(
                str(era_mismatch.queryEra), str(era_mismatch.ledgerEra)
            )
        elif is_pools_ranking(query_response):
            return query_response.result
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
