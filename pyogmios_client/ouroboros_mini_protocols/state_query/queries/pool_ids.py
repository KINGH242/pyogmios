from typing import List

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import EraMismatch, PoolId
from pyogmios_client.models.response_model import PoolIdsResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_era_mismatch(response: PoolIdsResponse) -> bool:
    if isinstance(response, EraMismatch):
        return response.eraMismatch is not None


def is_pool_ids(response: PoolIdsResponse) -> bool:
    result = response.result
    if isinstance(result, List) and len(result) > 0:
        if isinstance(result[0], PoolId):
            return True
    return False


async def pool_ids(context: InteractionContext) -> List[PoolId]:
    request_args = RequestArgs(method_name=MethodName.QUERY, args={"query": "poolIds"})

    try:
        response = await query(request_args, context)
        query_response = PoolIdsResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("poolIds")
        elif is_era_mismatch(query_response):
            era_mismatch = response.result.eraMismatch
            raise EraMismatchError(
                str(era_mismatch.queryEra), str(era_mismatch.ledgerEra)
            )
        elif is_pool_ids(query_response):
            return query_response.result
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
