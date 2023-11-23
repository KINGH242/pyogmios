from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import QueryUnavailableInCurrentEraError
from pyogmios_client.models import PointOrOrigin
from pyogmios_client.models.response_model import ChainTipResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


async def chain_tip(context: InteractionContext) -> PointOrOrigin:
    """
    Query the current chain tip.
    :param context: The interaction context to use for the query.
    :return: The current chain tip.
    """
    request_args = RequestArgs(method_name=MethodName.QUERY, args={"query": "chainTip"})

    try:
        response = await query(request_args, context)
        query_response = ChainTipResponse(**response.model_dump())
        result = query_response.result
        if hasattr(result, "root") and result.root == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("chainTip")
        return result
    except Exception as error:
        raise error
