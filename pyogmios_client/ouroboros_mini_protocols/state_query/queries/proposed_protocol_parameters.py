from typing import Dict

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
)
from pyogmios_client.models import (
    EraMismatch,
    ProtocolParametersBabbage,
    ProtocolParametersAlonzo,
    ProtocolParametersShelley,
)
from pyogmios_client.models.response_model import PoolsRankingResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_era_mismatch(response: PoolsRankingResponse) -> bool:
    if isinstance(response, EraMismatch):
        return response.eraMismatch is not None


async def proposed_protocol_parameters(
    context: InteractionContext,
) -> Dict[str, ProtocolParametersShelley] | Dict[str, ProtocolParametersAlonzo] | Dict[
    str, ProtocolParametersBabbage
] | None:
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "proposedProtocolParameters"}
    )

    try:
        response = await query(request_args, context)
        query_response = PoolsRankingResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("proposedProtocolParameters")
        elif is_era_mismatch(query_response):
            era_mismatch = response.result.eraMismatch
            raise EraMismatchError(
                str(era_mismatch.queryEra), str(era_mismatch.ledgerEra)
            )
        else:
            return query_response.result
    except Exception as error:
        raise error
