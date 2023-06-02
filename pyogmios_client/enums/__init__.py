from enum import Enum


class AcquireFailureDetails(Enum):
    POINT_TOO_OLD = "pointTooOld"
    POINT_NOT_ON_CHAIN = "pointNotOnChain"


class InputSource(Enum):
    INPUTS = "inputs"
    COLLATERALS = "collaterals"


class Language(Enum):
    PLUTUS_V_1 = "plutus:v1"
    PLUTUS_V_2 = "plutus:v2"


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


class Network(Enum):
    MAINNET = "mainnet"
    TESTNET = "testnet"


class NonceEnum(Enum):
    NEUTRAL = "neutral"


# class Origin(Enum):
#     ORIGIN = 'origin'
class Origin(Enum):
    origin = "origin"


class RewardPot(Enum):
    RESERVES = "reserves"
    TREASURY = "treasury"


class ServiceName(Enum):
    OGMIOS = "ogmios"


class Type(Enum):
    JSONWSP_REQUEST = "jsonwsp/request"
    JSONWSP_RESPONSE = "jsonwsp/response"
    JSONWSP_FAULT = "jsonwsp/fault"


class Version(Enum):
    v1_0 = "1.0"


class InvalidEntityType(Enum):
    ADDRESS = "address"
    POOL_REGISTRATION = "poolRegistration"
    REWARD_ACCOUNT = "rewardAccount"


class InvalidEntityEntity(Enum):
    ADDRESS = "Address"
    POOL_REGISTRATION = "PoolId"
    REWARD_ACCOUNT = "RewardAccount"
