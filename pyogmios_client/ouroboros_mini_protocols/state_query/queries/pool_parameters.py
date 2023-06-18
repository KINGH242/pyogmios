from typing import List, Dict

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import EraMismatch, PoolId, PoolParameters
from pyogmios_client.models.response_model import PoolParametersResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_era_mismatch(response: PoolParametersResponse) -> bool:
    if isinstance(response, EraMismatch):
        return response.eraMismatch is not None


def is_pool_parameters(response: PoolParametersResponse) -> bool:
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
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": {"poolParameters": pools}}
    )

    try:
        response = await query(request_args, context)
        query_response = PoolParametersResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("poolParameters")
        elif is_era_mismatch(query_response):
            era_mismatch = response.result.eraMismatch
            raise EraMismatchError(
                str(era_mismatch.queryEra), str(era_mismatch.ledgerEra)
            )
        elif is_pool_parameters(query_response):
            return query_response.result
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
