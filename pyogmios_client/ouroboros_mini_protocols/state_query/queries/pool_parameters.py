from typing import List, Dict

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import (
    PoolId,
    PoolParameters,
    EraMismatch,
    QueryUnavailableInCurrentEra,
)
from pyogmios_client.models.response_model import PoolParametersResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


async def pool_parameters(
    context: InteractionContext, pools: List[PoolId]
) -> Dict[str, PoolParameters]:
    """
    Query the pool parameters.
    :param context: The interaction context to use for the query.
    :param pools: The list of pool ids to query.
    :return: The pool parameters.
    """
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": {"poolParameters": pools}}
    )

    try:
        response = await query(request_args, context)
        query_response = PoolParametersResponse(**response.model_dump())
        result = query_response.result
        if isinstance(result, QueryUnavailableInCurrentEra):
            raise QueryUnavailableInCurrentEraError("poolParameters")
        elif isinstance(result, EraMismatch):
            raise EraMismatchError(result.queryEra.value, result.ledgerEra.value)
        elif isinstance(result, Dict):
            return result
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
