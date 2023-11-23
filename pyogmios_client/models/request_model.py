from __future__ import annotations

from typing import Optional, Dict, Any

from pydantic import Field

from pyogmios_client.enums import MethodName, ServiceName, Type, Version
from pyogmios_client.models.base_request_response_model import BaseRequestResponse


class Request(BaseRequestResponse):
    args: Optional[Dict[str, Any]] = None
    mirror: Optional[Any] = Field(
        None,
        description="An arbitrary JSON value that will be mirrored back in the response.",
    )

    @staticmethod
    def from_base_request(
        method_name: MethodName,
        args: Optional[Dict[str, Any]] = None,
        mirror: Optional[Any] = None,
    ) -> Request:
        return Request(
            type=Type.JSONWSP_REQUEST,
            version=Version.v1_0,
            servicename=ServiceName.OGMIOS,
            methodname=method_name,
            args=args,
            mirror=mirror,
        )


class RequestNext(BaseRequestResponse):
    methodname: MethodName = MethodName.REQUEST_NEXT

    @staticmethod
    def from_base(
        args: Optional[Dict[str, Any]] = None,
        mirror: Optional[Any] = None,
    ) -> RequestNext:
        return RequestNext(
            **Request.from_base_request(
                method_name=MethodName.REQUEST_NEXT,
                args=args,
                mirror=mirror,
            ).model_dump()
        )


class RequestRelease(BaseRequestResponse):
    methodname: MethodName = MethodName.RELEASE

    @staticmethod
    def from_base(
        args: Optional[Dict[str, Any]] = None,
        mirror: Optional[Any] = None,
    ) -> RequestRelease:
        return RequestRelease(
            **Request.from_base_request(
                method_name=MethodName.RELEASE,
                args=args,
                mirror=mirror,
            ).model_dump()
        )


class RequestAwaitAcquire(BaseRequestResponse):
    methodname: MethodName = MethodName.AWAIT_ACQUIRE

    @staticmethod
    def from_base(
        args: Optional[Dict[str, Any]] = None,
        mirror: Optional[Any] = None,
    ) -> RequestAwaitAcquire:
        return RequestAwaitAcquire(
            **Request.from_base_request(
                method_name=MethodName.AWAIT_ACQUIRE,
                args=args,
                mirror=mirror,
            ).model_dump()
        )
