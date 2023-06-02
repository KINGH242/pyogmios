from typing import List

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    UnknownResultError,
    IntersectionNotFoundError,
    TipIsOriginError,
)
from pyogmios_client.models import Point, PointOrOrigin, Origin
from pyogmios_client.models.result_models import IntersectionFound
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    RequestArgs,
    query,
)


async def find_intersect(
    context: InteractionContext, points: List[PointOrOrigin]
) -> IntersectionFound:
    request_args = RequestArgs(
        method_name=MethodName.FIND_INTERSECT, args={"points": points}
    )

    try:
        response = await query(request_args, context)
        if response.methodname is not MethodName.FIND_INTERSECT:
            raise UnknownResultError(response)
        if response.result.IntersectionFound:
            return response.result.IntersectionFound
        elif response.result.IntersectionNotFound:
            raise IntersectionNotFoundError(response.result.IntersectionNotFound.tip)
    except IntersectionNotFoundError as e:
        raise IntersectionNotFoundError(points) from e


async def create_point_from_current_tip(context: InteractionContext) -> Point:
    origin = Origin()
    intersect = await find_intersect(context, [origin])
    tip = intersect.tip
    if tip == origin.__root__:
        raise TipIsOriginError()
    return Point(slot=tip.slot, hash=tip.hash)
