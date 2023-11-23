from typing import List

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import PoolId, EraMismatch, QueryUnavailableInCurrentEra
from pyogmios_client.models.response_model import PoolIdsResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_pool_ids(response: PoolIdsResponse) -> bool:
    """
    Check if the response is a list of pool ids.
    :param response: The response to check.
    :return: True if the response is a list of pool ids, False otherwise.
    """
    result = response.result
    return (
        isinstance(result, List) and len(result) > 0 and isinstance(result[0], PoolId)
    )


async def pool_ids(context: InteractionContext) -> List[PoolId]:
    """
    Query the pool ids.
    :param context: The interaction context to use for the query.
    :return: The pool ids.
    """
    request_args = RequestArgs(method_name=MethodName.QUERY, args={"query": "poolIds"})

    try:
        response = await query(request_args, context)
        query_response = PoolIdsResponse(**response.model_dump())
        result = query_response.result
        if isinstance(result, QueryUnavailableInCurrentEra):
            raise QueryUnavailableInCurrentEraError("poolIds")
        elif isinstance(result, EraMismatch):
            raise EraMismatchError(result.queryEra.value, result.ledgerEra.value)
        elif is_pool_ids(query_response):
            return query_response.result
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
