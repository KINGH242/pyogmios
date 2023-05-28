from typing import List

from promise import Promise

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums.method_name_enum import MethodName
from pyogmios_client.exceptions import (
    UnknownResultError,
    IntersectionNotFoundError,
    TipIsOriginError,
)
from pyogmios_client.models.base_model import BaseModel
from pyogmios_client.models.point_model import Point, PointOrOrigin, TipOrOrigin, Origin
from pyogmios_client.models.response_model import FindIntersectResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    RequestArgs,
    query,
    ResponseArgs,
)


class Intersection(BaseModel):
    point: PointOrOrigin
    tip: TipOrOrigin


async def find_intersect(
    context: InteractionContext, points: List[PointOrOrigin]
) -> Promise[Intersection]:
    request_args = RequestArgs(
        method_name=MethodName.FIND_INTERSECT, args={"points": points}
    )

    def handler(query_response: FindIntersectResponse, resolve, reject):
        if query_response.method_name is MethodName.FIND_INTERSECT:
            if query_response.result.intersection_found:
                return resolve(query_response.result.intersection_found)
            elif query_response.result.intersection_not_found:
                reject(IntersectionNotFoundError(points))
        else:
            reject(UnknownResultError(query_response))

    response_args = ResponseArgs(handler=handler)
    response = await query(request_args, response_args, context)

    return Promise(lambda resolve, reject: resolve(response))


async def create_point_from_current_tip(context: InteractionContext) -> Point:
    intersect = await find_intersect(context, [Origin])
    tip = intersect.get().tip
    if tip == Origin:
        raise TipIsOriginError()
    return Point(slot=tip.slot, hash=tip.hash)
