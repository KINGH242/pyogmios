from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import (
    ProtocolParametersBabbage,
    ProtocolParametersAlonzo,
    ProtocolParametersShelley,
    QueryUnavailableInCurrentEra,
)
from pyogmios_client.models.response_model import CurrentProtocolParametersResponse
from pyogmios_client.models.result_models import EraMismatchResult
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_protocol_parameters(response: CurrentProtocolParametersResponse) -> bool:
    """
    Check if the response is a protocol parameters response.
    :param response: The response to check.
    :return: True if the response is a protocol parameters response, False otherwise.
    """
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
    """
    Query the current protocol parameters.
    :param context: The interaction context to use for the query.
    :return: The current protocol parameters.
    """
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "currentProtocolParameters"}
    )

    try:
        response = await query(request_args, context)
        query_response = CurrentProtocolParametersResponse(**response.model_dump())
        result = query_response.result
        if isinstance(result, QueryUnavailableInCurrentEra):
            raise QueryUnavailableInCurrentEraError("currentProtocolParameters")
        elif is_protocol_parameters(query_response):
            return query_response.result
        elif isinstance(result, EraMismatchResult):
            era_mismatch = result.eraMismatch
            raise EraMismatchError(
                era_mismatch.queryEra.value, era_mismatch.ledgerEra.value
            )
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
