from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import Epoch, QueryUnavailableInCurrentEra
from pyogmios_client.models.response_model import CurrentEpochResponse
from pyogmios_client.models.result_models import EraMismatchResult
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


async def current_epoch(context: InteractionContext) -> Epoch:
    """
    Query the current epoch.
    :param context: The interaction context to use for the query.
    :return: The current epoch.
    """
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "currentEpoch"}
    )

    try:
        response = await query(request_args, context)
        query_response = CurrentEpochResponse(**response.model_dump())
        result = query_response.result
        if isinstance(result, QueryUnavailableInCurrentEra):
            raise QueryUnavailableInCurrentEraError("currentEpoch")
        elif isinstance(result, Epoch):
            return result
        elif isinstance(result, EraMismatchResult):
            era_mismatch = result.eraMismatch
            raise EraMismatchError(
                era_mismatch.queryEra.value, era_mismatch.ledgerEra.value
            )
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
