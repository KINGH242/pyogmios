from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import EraMismatch, Origin, PointOrOrigin, Point
from pyogmios_client.models.response_model import LedgerTipResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_era_mismatch(response: LedgerTipResponse) -> bool:
    if isinstance(response, EraMismatch):
        return response.eraMismatch is not None


def is_non_origin_point(response: LedgerTipResponse) -> bool:
    result = response.result
    if isinstance(result, Point):
        return result.slot is not None and result.hash is not None
    return False


async def ledger_tip(context: InteractionContext) -> PointOrOrigin:
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "ledgerTip"}
    )

    try:
        response = await query(request_args, context)
        query_response = LedgerTipResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("ledgerTip")
        elif isinstance(query_response.result, Origin):
            return query_response.result
        elif is_era_mismatch(query_response):
            era_mismatch = response.result.eraMismatch
            raise EraMismatchError(
                str(era_mismatch.queryEra), str(era_mismatch.ledgerEra)
            )
        elif is_non_origin_point(query_response):
            return query_response.result
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
