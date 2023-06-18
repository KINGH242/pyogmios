from typing import List

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    UnknownResultError,
    IntersectionNotFoundError,
    TipIsOriginError,
)
from pyogmios_client.models import Point, PointOrOrigin, Origin
from pyogmios_client.models.response_model import FindIntersectResponse
from pyogmios_client.models.result_models import IntersectionFound
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    RequestArgs,
    query,
)


async def find_intersect(
    context: InteractionContext, points: List[PointOrOrigin]
) -> IntersectionFound:
    """
    Find intersect.
    :param context: The interaction context
    :param points: The points
    :return: The intersection found
    """
    request_args = RequestArgs(
        method_name=MethodName.FIND_INTERSECT, args={"points": points}
    )

    try:
        response = await query(request_args, context)
        find_intersect_response = FindIntersectResponse(**response.dict())
        if find_intersect_response.methodname is not MethodName.FIND_INTERSECT:
            raise UnknownResultError(find_intersect_response)
        if find_intersect_response.result.IntersectionFound:
            return find_intersect_response.result.IntersectionFound
        elif find_intersect_response.result.IntersectionNotFound:
            raise IntersectionNotFoundError(
                find_intersect_response.result.IntersectionNotFound.tip
            )
    except IntersectionNotFoundError as e:
        raise IntersectionNotFoundError(points) from e


async def create_point_from_current_tip(context: InteractionContext) -> Point:
    """
    Create point from current tip.
    :param context: The interaction context
    :return: The point
    """
    origin = Origin()
    intersect = await find_intersect(context, [origin])
    tip = intersect.tip
    if tip == origin.__root__:
        raise TipIsOriginError()
    return Point(slot=tip.slot, hash=tip.hash)
