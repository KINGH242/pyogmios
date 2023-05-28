from __future__ import annotations

from typing import Optional, Dict, Any

from pydantic import Field

from pyogmios_client.enums.method_name_enum import MethodName
from pyogmios_client.enums.service_name_enum import ServiceName
from pyogmios_client.enums.type_enum import Type
from pyogmios_client.enums.version_enum import Version
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
            service_name=ServiceName.OGMIOS,
            method_name=method_name,
            args=args,
            mirror=mirror,
        )
