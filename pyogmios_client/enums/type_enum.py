from enum import Enum


class Type(Enum):
    JSONWSP_REQUEST = "jsonwsp/request"
    JSONWSP_RESPONSE = "jsonwsp/response"
    JSONWSP_FAULT = "jsonwsp/fault"
