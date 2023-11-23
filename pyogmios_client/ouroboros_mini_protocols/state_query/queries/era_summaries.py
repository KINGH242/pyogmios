from typing import List

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import UnknownResultError
from pyogmios_client.models import EraSummary
from pyogmios_client.models.response_model import EraSummariesResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


async def era_summaries(context: InteractionContext) -> List[EraSummary]:
    """
    Query the era summaries.
    :param context: The interaction context to use for the query.
    :return: The era summaries.
    """
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "eraSummaries"}
    )

    try:
        response = await query(request_args, context)
        query_response = EraSummariesResponse(**response.model_dump())
        if isinstance(query_response.result, List):
            return query_response.result
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
