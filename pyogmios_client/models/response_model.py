from __future__ import annotations

from abc import ABC
from typing import Optional, Any, Dict

from pydantic import Field, Extra

from pyogmios_client.enums import MethodName, ServiceName, Type, Version
from pyogmios_client.models import BaseModel
from pyogmios_client.models.base_request_response_model import BaseRequestResponse
from pyogmios_client.models.result_models import Result


class Response(ABC, BaseRequestResponse):
    result: Optional[Result]
    fault: Optional[Dict[str, Any]]
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
            servicename=ServiceName.OGMIOS,
            methodname=method_name,
            result=result,
            reflection=reflection,
        )


class QueryResponseReflection(BaseModel):
    class Config:
        extra = Extra.allow

    requestId: Optional[str]


class QueryResponse(Response, ABC):
    reflection: Optional[QueryResponseReflection]


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
