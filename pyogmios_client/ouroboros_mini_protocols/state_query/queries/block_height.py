from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import QueryUnavailableInCurrentEraError
from pyogmios_client.models import BlockNoOrOrigin
from pyogmios_client.models.response_model import QueryResponseBlockHeight
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


async def block_height(context: InteractionContext) -> BlockNoOrOrigin:
    """
    Query the current block height.
    :param context: The interaction context to use for the query.
    :return: The current block height number or origin.
    """
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "blockHeight"}
    )

    try:
        response = await query(request_args, context)
        print(response.dict())
        query_response = QueryResponseBlockHeight(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("blockHeight")
        return response.result
    except Exception as error:
        raise error
