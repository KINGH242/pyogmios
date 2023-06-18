from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import (
    EraMismatch,
    ProtocolParametersBabbage,
    ProtocolParametersAlonzo,
    ProtocolParametersShelley,
)
from pyogmios_client.models.response_model import CurrentProtocolParametersResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_era_mismatch(response: CurrentProtocolParametersResponse) -> bool:
    if isinstance(response, EraMismatch):
        return response.eraMismatch is not None


def is_protocol_parameters(response: CurrentProtocolParametersResponse) -> bool:
    result = response.result
    if isinstance(result, ProtocolParametersBabbage):
        return result.coinsPerUtxoByte is not None
    elif isinstance(result, ProtocolParametersAlonzo):
        return result.coinsPerUtxoWord is not None
    elif isinstance(result, ProtocolParametersShelley):
        return result.minUtxoValue is not None


async def current_protocol_parameters(
    context: InteractionContext,
) -> ProtocolParametersBabbage | ProtocolParametersAlonzo | ProtocolParametersShelley:
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "currentProtocolParameters"}
    )

    try:
        response = await query(request_args, context)
        query_response = CurrentProtocolParametersResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("currentProtocolParameters")
        elif is_protocol_parameters(query_response):
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
