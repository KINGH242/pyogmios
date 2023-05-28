from enum import Enum


class MethodName(Enum):
    REQUEST_NEXT = "RequestNext"
    FIND_INTERSECT = "FindIntersect"
    SUBMIT_TX = "SubmitTx"
    EVALUATE_TX = "EvaluateTx"
    ACQUIRE = "Acquire"
    RELEASE = "Release"
    AWAIT_ACQUIRE = "AwaitAcquire"
    NEXT_TX = "NextTx"
    HAS_TX = "HasTx"
    SIZE_AND_CAPACITY = "SizeAndCapacity"
    RELEASE_MEMPOOL = "ReleaseMempool"
    QUERY = "Query"
