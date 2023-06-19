from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import Origin, PointOrOrigin, Point
from pyogmios_client.models.response_model import LedgerTipResponse
from pyogmios_client.models.result_models import EraMismatchResult
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_non_origin_point(response: LedgerTipResponse) -> bool:
    """
    Check if the response is a non-origin point.
    :param response: The response to check.
    :return: True if the response is a non-origin point, False otherwise.
    """
    result = response.result
    if isinstance(result, Point):
        return result.slot is not None and result.hash is not None
    return False


async def ledger_tip(context: InteractionContext) -> PointOrOrigin:
    """
    Query the current ledger tip.
    :param context: The interaction context to use for the query.
    :return: The current ledger tip.
    """
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "ledgerTip"}
    )

    try:
        response = await query(request_args, context)
        query_response = LedgerTipResponse(**response.dict())
        result = query_response.result
        if result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("ledgerTip")
        elif isinstance(result, Origin):
            return result
        elif isinstance(result, EraMismatchResult):
            era_mismatch = result.eraMismatch
            raise EraMismatchError(
                str(era_mismatch.queryEra), str(era_mismatch.ledgerEra)
            )
        elif is_non_origin_point(query_response):
            return query_response.result
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
