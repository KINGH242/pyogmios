from __future__ import annotations

from pyogmios_client.enums.method_name_enum import MethodName
from pyogmios_client.enums.service_name_enum import ServiceName
from pyogmios_client.enums.type_enum import Type
from pyogmios_client.enums.version_enum import Version
from pyogmios_client.models.base_model import BaseModel


class BaseRequestResponse(BaseModel):
    type: Type
    version: Version
    service_name: ServiceName
    method_name: MethodName
