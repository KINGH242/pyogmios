from typing import Optional

import aiohttp
from pyogmios_client.models.base_model import BaseModel

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
    """
    Checks the server health.
    :param options: The options
    :return: The server health or an error
    """
    url = f"{options.connection.address.http}/health"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url)
        if response.status == 200:
            server_health = ServerHealth(**await response.json())
        else:
            raise RequestError(f"Error: {response.status}")

    return server_health
