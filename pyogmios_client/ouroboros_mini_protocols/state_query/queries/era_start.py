from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import UnknownResultError
from pyogmios_client.models import Bound
from pyogmios_client.models.response_model import EraStartResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_bound(response: EraStartResponse) -> bool:
    bound = response.result
    if isinstance(bound, Bound):
        return (
            bound.time is not None
            and bound.slot is not None
            and bound.epoch is not None
        )


async def era_start(context: InteractionContext) -> Bound:
    request_args = RequestArgs(method_name=MethodName.QUERY, args={"query": "eraStart"})

    try:
        response = await query(request_args, context)
        query_response = EraStartResponse(**response.dict())
        if is_bound(query_response):
            return query_response.result
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
