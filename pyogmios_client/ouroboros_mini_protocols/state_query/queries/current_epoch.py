from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import Epoch, EraMismatch
from pyogmios_client.models.response_model import CurrentEpochResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_era_mismatch(response: CurrentEpochResponse) -> bool:
    if isinstance(response, EraMismatch):
        return response.eraMismatch is not None


async def current_epoch(context: InteractionContext) -> Epoch:
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "currentEpoch"}
    )

    try:
        response = await query(request_args, context)
        query_response = CurrentEpochResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("currentEpoch")
        elif isinstance(query_response.result, Epoch):
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
