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


class InteractionContextFactory(ModelFactory):
    __model__ = InteractionContext


class ServerHealthFactory(ModelFactory):
    __model__ = ServerHealth


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
