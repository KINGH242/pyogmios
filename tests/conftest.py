from unittest.mock import AsyncMock

import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from pyogmios_client.connection import InteractionContext
from pyogmios_client.models import (
    ProtocolParametersShelley,
    ProtocolParametersBabbage,
    ProtocolParametersAlonzo,
    GenesisAlonzo,
    GenesisByron,
    GenesisShelley,
    PoolParameters,
    RewardsProvenance,
    RewardsProvenanceNew,
)
from pyogmios_client.models.request_model import Request
from pyogmios_client.models.result_models import EraMismatchResult, FindIntersectResult
from pyogmios_client.models.server_health_model import ServerHealth
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    RequestArgs,
    ResponseArgs,
    ResponseHandlerArgs,
)
from pyogmios_client.server_health import ConnectionConfig, Connection, Options, Address


class ConnectionConfigFactory(ModelFactory):
    __model__ = ConnectionConfig


class ConnectionFactory(ModelFactory):
    __model__ = Connection


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


class ProtocolParametersShelleyFactory(ModelFactory):
    __model__ = ProtocolParametersShelley


class ProtocolParametersAlonzoFactory(ModelFactory):
    __model__ = ProtocolParametersAlonzo


class ProtocolParametersBabbageFactory(ModelFactory):
    __model__ = ProtocolParametersBabbage


class GenesisAlonzoFactory(ModelFactory):
    __model__ = GenesisAlonzo


class GenesisByronFactory(ModelFactory):
    __model__ = GenesisByron


class GenesisShelleyFactory(ModelFactory):
    __model__ = GenesisShelley


class EraMismatchResultFactory(ModelFactory):
    __model__ = EraMismatchResult


class PoolParametersFactory(ModelFactory):
    __model__ = PoolParameters


class RewardsProvenanceFactory(ModelFactory):
    __model__ = RewardsProvenance


class RewardsProvenanceNewFactory(ModelFactory):
    __model__ = RewardsProvenanceNew


class FindIntersectResultFactory(ModelFactory):
    __model__ = FindIntersectResult


@pytest.fixture(autouse=True)
def mock_server_health(mocker):
    """
    Fixture for mocking the get_server_health function
    """
    async_mock = AsyncMock(return_value=ServerHealthFactory.build())
    mocker.patch(
        "pyogmios_client.connection.get_server_health",
        return_value=async_mock,
    )
    mocker.patch(
        "pyogmios_client.utils.socket_utils.ensure_socket_is_open", return_value=True
    )
    mocker.patch("threading.Thread")
    mocker.patch("threading.Event.is_set", return_value=True)
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.chain_sync.request_next.request_next"
    )
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client.ensure_socket_is_open"
    )


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


@pytest.fixture
def mock_server_health_options():
    """
    Fixture for the Server Health Options object
    """
    return Options(
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


@pytest.fixture
def fake_query_response():
    """
    Fixture for a fake query response
    """
    return {
        "type": "jsonwsp/response",
        "version": "1.0",
        "methodname": "Query",
        "result": "test-result",
        "reflection": {"mirror": "test-mirror", "requestId": "test-request-id"},
    }


@pytest.fixture
def fake_era_mismatch_result():
    """
    Fixture for a fake era mismatch response
    """
    return {"eraMismatch": {"queryEra": "Byron", "ledgerEra": "Mary"}}


@pytest.fixture
def fake_non_myopic_member_rewards():
    return {
        "1000000": {
            "pool1qqqqqdk4zhsjuxxd8jyvwncf5eucfskz0xjjj64fdmlgj735lr9": 688,
            "pool1qqqqpanw9zc0rzh0yp247nzf2s35uvnsm7aaesfl2nnejaev0uc": 676,
            "pool1qqqqzyqf8mlm70883zht60n4q6uqxg4a8x266sewv8ad2grkztl": 0,
        },
        "bc1597ad71c55d2d009a9274b3831ded155118dd769f5376decc1369": {
            "pool1qfzjwrtupyvzx0atp5pa3m82v7s8z2eqyqffa0grpyf4j349h6r": 0,
            "pool1qfxukshs4fkcrflzdnxa2fdza5lfvew3y6echg8ckaa4q8m5hyf": 103181546,
        },
    }


@pytest.fixture
def fake_delegations_and_rewards_by_accounts():
    """
    Fixture for a fake delegations and rewards by accounts
    """
    return {
        "bc1597ad71c55d2d009a9274b3831ded155118dd769f5376decc1369": {
            "delegate": "pool1kchver88u3kygsak8wgll7htr8uxn5v35lfrsyy842nkscrzyvj",
            "rewards": 219558722,
        }
    }


@pytest.fixture
def fake_find_intersect_intersect_found_result():
    """
    Fixture for a fake find intersect response
    """
    return {
        "result": {
            "IntersectionFound": {
                "point": {
                    "slot": 18446744073709552000,
                    "hash": "c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d",
                },
                "tip": {
                    "slot": 18446744073709552000,
                    "hash": "c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d",
                    "blockNo": 18446744073709552000,
                },
            }
        }
    }
