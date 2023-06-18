from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import QueryUnavailableInCurrentEraError
from pyogmios_client.models import UtcTime
from pyogmios_client.models.response_model import SystemStartResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


async def system_start(context: InteractionContext) -> UtcTime:
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "systemStart"}
    )

    try:
        response = await query(request_args, context)
        query_response = SystemStartResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("systemStart")
        else:
            return query_response.result
    except Exception as error:
        raise error
