from typing import List

from pyogmios_client.models import PointOrOrigin


class ServerNotReady(Exception):
    def __init__(self, health):
        self.health = health
        self.message = (
            f"Server not ready. Network synchronization at: {health.network_sync_at}"
        )
        super().__init__(self.message)


class RequestError(Exception):
    def __init__(self, response):
        self.response = response
        self.message = f"Request error: {response.status}"
        super().__init__(self.message)


class IntersectionNotFoundError(Exception):
    def __init__(self, points: PointOrOrigin | List[PointOrOrigin]):
        self.points = points
        self.message = f"Intersection with points {points.json()} not found"
        super().__init__(self.message)


class UnknownResultError(Exception):
    def __init__(self, result):
        self.result = result
        self.message = f"Unknown result error: {result}"
        super().__init__(self.message)


class TipIsOriginError(Exception):
    def __init__(self):
        self.message = "Unable to produce point as the chain tip is the origin"
        super().__init__(self.message)


class WebSocketClosedError(Exception):
    def __init__(self):
        self.message = "WebSocket is closed"
        super().__init__(self.message)


class QueryUnavailableInCurrentEraError(Exception):
    def __init__(self, query_name):
        self.query_name = query_name
        self.message = f"QueryUnavailableInCurrentEra. {query_name}"
        super().__init__(self.message)


class AcquirePointTooOldError(Exception):
    def __init__(self):
        self.message = "Acquire point too old"
        super().__init__(self.message)


class AcquirePointNotOnChainError(Exception):
    def __init__(self):
        self.message = "Acquire point not on chain"
        super().__init__(self.message)


class AcquirePointFailureError(Exception):
    def __init__(self, failure):
        self.failure = failure
        self.message = f"Unknown AcquirePointFailure ${failure}"
        super().__init__(self.message)


class EraMismatchError(Exception):
    def __init__(self, query_era: str, ledger_era: str):
        self.query_era = query_era
        self.ledger_era = ledger_era
        self.message = (
            f"Era mismatch. Query from era {query_era}. Ledger is in {ledger_era}"
        )
        super().__init__(self.message)
