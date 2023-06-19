import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from pyogmios_client.connection import InteractionContext
from pyogmios_client.models.request_model import Request
from pyogmios_client.models.server_health_model import ServerHealth
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    RequestArgs,
    ResponseArgs,
    ResponseHandlerArgs,
)
from pyogmios_client.server_health import ConnectionConfig


class ConnectionConfigFactory(ModelFactory):
    __model__ = ConnectionConfig


class RequestFactory(ModelFactory):
    __model__ = Request


class RequestArgsFactory(ModelFactory):
    __model__ = RequestArgs


class ResponseHandlerArgsFactory(ModelFactory):
    __model__ = ResponseHandlerArgs


class ResponseArgsFactory(ModelFactory):
    __model__ = ResponseArgs


class ServerHealthFactory(ModelFactory):
    __model__ = ServerHealth


class InteractionContextFactory(ModelFactory):
    __model__ = InteractionContext


@pytest.fixture
async def mock_server_health_response(monkeypatch):
    def mock_json_response(request):
        return {
            "startTime": "2023-05-26T02:41:33.278462Z",
            "lastKnownTip": {
                "slot": 93709629,
                "hash": "693fe3ebc342fb15f093b4dea3cfd35d6abbc82dcec9cf30468fc97a3fb21420",
                "blockNo": 8831574,
            },
            "lastTipUpdate": "2023-05-28T12:12:01.134132Z",
            "networkSynchronization": 1,
            "currentEra": "Babbage",
            "metrics": {
                "activeConnections": 0,
                "runtimeStats": {
                    "cpuTime": 219771946000,
                    "currentHeapSize": 1032,
                    "gcCpuTime": 202336910000,
                    "maxHeapSize": 1225,
                },
                "sessionDurations": {"max": 0, "mean": 509985.0294117646, "min": 0},
                "totalConnections": 34,
                "totalMessages": 278,
                "totalUnrouted": 4,
            },
            "connectionStatus": "connected",
            "currentEpoch": 414,
            "slotInEpoch": 224829,
        }

    monkeypatch.setattr("aiohttp.web.json_response", mock_json_response)


@pytest.fixture
def mock_send(monkeypatch):
    def mock_send(self, *args, **kwargs):
        return kwargs

    monkeypatch.setattr("pyogmios_client.request.send", mock_send)


@pytest.fixture
def fake_server_health():
    """
    Fixture for a fake server health response
    """
    return {
        "startTime": "2023-06-18T23:18:44.597761Z",
        "lastKnownTip": {
            "slot": 95564600,
            "hash": "36881dc2a6e2e998d168e40048522a9b89a441d8702283501f0bbc64e0611f16",
            "blockNo": 8921790,
        },
        "lastTipUpdate": "2023-06-18T23:28:11.742438Z",
        "networkSynchronization": 1,
        "currentEra": "Babbage",
        "metrics": {
            "activeConnections": 0,
            "runtimeStats": {
                "cpuTime": 1154541000,
                "currentHeapSize": 354,
                "gcCpuTime": 682582000,
                "maxHeapSize": 367,
            },
            "sessionDurations": {"max": 0, "mean": 0, "min": 0},
            "totalConnections": 0,
            "totalMessages": 0,
            "totalUnrouted": 0,
        },
        "connectionStatus": "connected",
        "currentEpoch": 418,
        "slotInEpoch": 351800,
    }
