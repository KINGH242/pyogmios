from __future__ import annotations

from abc import ABC
from typing import Optional

from pyogmios_client.enums import MethodName, ServiceName, Type, Version
from pyogmios_client.models.base_model import BaseModel


class BaseRequestResponse(ABC, BaseModel):
    type: Optional[Type]
    version: Optional[Version]
    servicename: Optional[ServiceName]
    methodname: Optional[MethodName]
