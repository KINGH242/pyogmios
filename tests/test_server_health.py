import pytest
from aiohttp import ClientConnectorError

from pyogmios_client.models.server_health_model import ServerHealth
from pyogmios_client.server_health import (
    Options,
    Connection,
    get_server_health,
    Address,
)


@pytest.mark.asyncio
async def test_get_server_health_success(mock_server_health_response):
    options = Options(
        connection=Connection(
            host="localhost",
            port=1337,
            tls=False,
            max_payload=1000,
            address=Address(
                http="http://localhost:1337", webSocket="ws://localhost:1337"
            ),
        )
    )
    server_health = await get_server_health(options=options)
    assert isinstance(server_health, ServerHealth)
    assert server_health.connection_status == "connected"


@pytest.mark.asyncio
async def test_get_server_health_error(mock_server_health_response):

    options = Options(
        connection=Connection(
            host="localhost",
            port=1000,
            tls=False,
            max_payload=1000,
            address=Address(
                http="http://notarealhost:1000", webSocket="ws://notarealhost:1000"
            ),
        )
    )
    with pytest.raises(ClientConnectorError):
        await get_server_health(options)
