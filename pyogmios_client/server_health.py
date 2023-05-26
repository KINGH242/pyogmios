from typing import Optional

import aiohttp
from models.base_model import BaseModel

from pyogmios_client.exceptions import RequestError
from pyogmios_client.models.server_health_model import ServerHealth


class ConnectionConfig(BaseModel):
    host: Optional[str]
    port: Optional[int]
    tls: Optional[bool]
    max_payload: Optional[int]


class Address(BaseModel):
    http: Optional[str]
    webSocket: Optional[str]


class Connection(ConnectionConfig):
    max_payload: int
    address: Address


class Options(BaseModel):
    connection: Connection


async def get_server_health(options: Options) -> ServerHealth | RequestError:
    async with aiohttp.ClientSession().get(f"{options.connection.address.http}/health") as response:
        if response.status == 200:
            return ServerHealth(**await response.json())
        else:
            raise RequestError(f"Error: {response.status}")
