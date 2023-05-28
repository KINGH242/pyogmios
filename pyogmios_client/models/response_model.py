from __future__ import annotations

from abc import ABC
from typing import Optional, Any, TypedDict

from pydantic import Field

from pyogmios_client.enums.method_name_enum import MethodName
from pyogmios_client.enums.service_name_enum import ServiceName
from pyogmios_client.enums.type_enum import Type
from pyogmios_client.enums.version_enum import Version
from pyogmios_client.models.base_request_response_model import BaseRequestResponse
from pyogmios_client.models.result_models import Result


class Response(ABC, BaseRequestResponse):
    result: Result
    reflection: Optional[Any] = Field(
        None,
        description="An arbitrary JSON value that will be mirrored back in the response.",
    )

    @staticmethod
    def from_base_response(
        method_name: MethodName, result: Result, reflection: Optional[Any] = None
    ) -> Response:
        return Response(
            type=Type.JSONWSP_RESPONSE,
            version=Version.v1_0,
            service_name=ServiceName.OGMIOS,
            method_name=method_name,
            result=result,
            reflection=reflection,
        )


class QueryResponse(ABC, Response):
    reflection: Optional[TypedDict("Reflection", {"request_id": str})]


class FindIntersectResponse(QueryResponse):
    @staticmethod
    def from_base(
        result: Result, reflection: Optional[Any] = None
    ) -> FindIntersectResponse:
        if result.intersection_found is None and result.intersection_not_found is None:
            raise ValueError(
                "Either intersection_found or intersection_not_found must be set."
            )
        return FindIntersectResponse(
            **Response.from_base_response(
                method_name=MethodName.FIND_INTERSECT,
                result=result,
                reflection=reflection,
            ).dict()
        )


class RequestNextResponse(QueryResponse):
    @staticmethod
    def from_base(
        result: Result, reflection: Optional[Any] = None
    ) -> RequestNextResponse:
        if result.roll_backward is None and result.roll_forward is None:
            raise ValueError("Either roll_backward or roll_forward must be set.")
        return RequestNextResponse(
            **Response.from_base_response(
                method_name=MethodName.REQUEST_NEXT,
                result=result,
                reflection=reflection,
            ).dict()
        )
