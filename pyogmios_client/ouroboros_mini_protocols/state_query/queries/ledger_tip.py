from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import PointOrOrigin, EraMismatch
from pyogmios_client.models.response_model import LedgerTipResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


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
        query_response = LedgerTipResponse(**response.model_dump())
        result = query_response.result
        if hasattr(result, "root") and result.root == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("ledgerTip")
        elif isinstance(result, PointOrOrigin):
            return result
        elif isinstance(result, EraMismatch):
            raise EraMismatchError(result.queryEra.value, result.ledgerEra.value)
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
