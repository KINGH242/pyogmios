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
    request_args = RequestArgs(method_name=MethodName.QUERY, args={"query": "chainTip"})

    try:
        response = await query(request_args, context)
        query_response = ChainTipResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("chainTip")
        return response.result
    except Exception as error:
        raise error
