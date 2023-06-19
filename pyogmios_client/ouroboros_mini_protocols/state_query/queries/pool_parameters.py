from typing import List, Dict

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import PoolId, PoolParameters
from pyogmios_client.models.response_model import PoolParametersResponse
from pyogmios_client.models.result_models import EraMismatchResult
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_pool_parameters(response: PoolParametersResponse) -> bool:
    """
    Check if the response is a list of pool parameters.
    :param response: The response to check.
    :return: True if the response is a list of pool parameters, False otherwise.
    """
    result = response.result
    if isinstance(result, Dict):
        # sample = list(result.values())[0]
        sample = next(iter(result))
        if isinstance(sample, PoolParameters):
            return True
    return False


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
        query_response = PoolParametersResponse(**response.dict())
        result = query_response.result
        if result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("poolParameters")
        elif isinstance(result, EraMismatchResult):
            era_mismatch = result.eraMismatch
            raise EraMismatchError(
                str(era_mismatch.queryEra), str(era_mismatch.ledgerEra)
            )
        elif is_pool_parameters(query_response):
            return query_response.result
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
