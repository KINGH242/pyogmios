from __future__ import annotations

from typing import Optional, Any, Dict, Union, List

from pydantic import Field, Extra

from pyogmios_client.enums import MethodName
from pyogmios_client.models import (
    BaseModel,
    BlockNoOrOrigin,
    QueryUnavailableInCurrentEra,
    PointOrOrigin,
    EraMismatch,
    Epoch,
    ProtocolParametersShelley,
    ProtocolParametersAlonzo,
    ProtocolParametersBabbage,
    DelegationsAndRewardsByAccounts,
    Bound,
    EraSummary,
    GenesisByron,
    GenesisShelley,
    GenesisAlonzo,
    NonMyopicMemberRewards,
    PoolId,
    PoolParameters,
    RewardsProvenance,
    RewardsProvenanceNew,
    UtcTime,
    Utxo,
    TxId,
    EvaluationResult,
    EvaluationFailure,
    PoolDistribution,
    PoolsRanking,
    TxAlonzo,
    TxBabbage,
    Null,
    MempoolSizeAndCapacity,
)
from pyogmios_client.models.base_request_response_model import BaseRequestResponse
from pyogmios_client.models.result_models import (
    SubmitTxError,
    RollForwardResult,
    RollBackwardResult,
    FindIntersectResult,
    AcquireSuccessResult,
    AcquireFailureResult,
    AwaitAcquiredResult,
    ReleaseResponseResult,
    EraMismatchResult,
)


class Response(BaseRequestResponse):
    fault: Optional[Dict[str, Any]]
    reflection: Optional[Any] = Field(
        None,
        description="An arbitrary JSON value that will be mirrored back in the response.",
    )

    class Config:
        extra = Extra.allow


class SubmitSuccess(BaseModel):
    class Config:
        extra = Extra.forbid

    txId: TxId


class SubmitTxResponseSubmitSuccess(BaseModel):
    SubmitSuccess: SubmitSuccess


class SubmitTxResponseSubmitFail(BaseModel):
    SubmitFail: SubmitTxError


class SubmitTxResponse(BaseModel):
    methodname: MethodName = MethodName.SUBMIT_TX
    result: Union[SubmitTxResponseSubmitSuccess, SubmitTxResponseSubmitFail]
    reflection: Optional[Dict[str, Any]]


class EvaluateTxResponse(BaseModel):
    methodname: MethodName = MethodName.EVALUATE_TX
    result: Union[EvaluationResult, EvaluationFailure]
    reflection: Optional[Dict[str, Any]]


class AwaitAcquireResponse(BaseModel):
    methodname: MethodName = MethodName.AWAIT_ACQUIRE
    result: AwaitAcquiredResult
    reflection: Optional[Dict[str, Any]]


class HasTxResponse(BaseModel):
    methodname: MethodName = MethodName.HAS_TX
    result: bool
    reflection: Optional[Dict[str, Any]]


class NextTxResponse(BaseModel):
    methodname: MethodName = MethodName.NEXT_TX
    result: Union[TxId, TxAlonzo, TxBabbage, Null]
    reflection: Optional[Dict[str, Any]]


class ReleaseMempoolResponse(BaseModel):
    methodname: MethodName = MethodName.RELEASE_MEMPOOL
    result: str
    reflection: Optional[Dict[str, Any]]


class SizeAndCapacityResponse(BaseModel):
    methodname: MethodName = MethodName.SIZE_AND_CAPACITY
    result: MempoolSizeAndCapacity
    reflection: Optional[Dict[str, Any]]


class QueryResponseReflection(BaseModel):
    requestId: Optional[str]


class QueryResponse(Response):
    methodname: MethodName = MethodName.QUERY
    reflection: Optional[QueryResponseReflection]


class FindIntersectResponse(QueryResponse):
    methodname: MethodName = MethodName.FIND_INTERSECT
    result: FindIntersectResult


class QueryResponseBlockHeight(QueryResponse):
    result: Union[BlockNoOrOrigin, QueryUnavailableInCurrentEra]


class RequestNextResponse(QueryResponse):
    result: Union[RollForwardResult, RollBackwardResult]


class ReleaseResponse(QueryResponse):
    methodname: MethodName = MethodName.RELEASE
    result: ReleaseResponseResult


class AcquireResponse(QueryResponse):
    methodname: MethodName = MethodName.ACQUIRE
    result = Union[AcquireSuccessResult, AcquireFailureResult]


class ChainTipResponse(QueryResponse):
    result: Optional[Union[PointOrOrigin, QueryUnavailableInCurrentEra]]


class CurrentEpochResponse(QueryResponse):
    result: Optional[Union[Epoch, EraMismatchResult, QueryUnavailableInCurrentEra]]


class CurrentProtocolParametersResponse(QueryResponse):
    result: Optional[
        Union[
            ProtocolParametersShelley,
            ProtocolParametersAlonzo,
            ProtocolParametersBabbage,
            EraMismatchResult,
            QueryUnavailableInCurrentEra,
        ]
    ]


class DelegationsAndRewardsResponse(QueryResponse):
    result: Optional[
        Union[
            DelegationsAndRewardsByAccounts,
            EraMismatchResult,
            QueryUnavailableInCurrentEra,
        ]
    ]


class EraStartResponse(QueryResponse):
    result: Optional[Union[Bound, QueryUnavailableInCurrentEra]]


class EraSummariesResponse(QueryResponse):
    result: Optional[Union[List[EraSummary], QueryUnavailableInCurrentEra]]


class GenesisConfigResponse(QueryResponse):
    result: Optional[
        Union[
            GenesisByron,
            GenesisShelley,
            GenesisAlonzo,
            EraMismatch,
            QueryUnavailableInCurrentEra,
        ]
    ]


class LedgerTipResponse(QueryResponse):
    result: Optional[Union[PointOrOrigin, EraMismatch, QueryUnavailableInCurrentEra]]


class NonMyopicMemberRewardsResponse(QueryResponse):
    result: Optional[
        Union[NonMyopicMemberRewards, EraMismatch, QueryUnavailableInCurrentEra]
    ]


class PoolIdsResponse(QueryResponse):
    result: Optional[Union[List[PoolId], EraMismatch, QueryUnavailableInCurrentEra]]


class PoolParametersResponse(QueryResponse):
    result: Optional[
        Union[Dict[str, PoolParameters], EraMismatch, QueryUnavailableInCurrentEra]
    ]


class PoolsRankingResponse(QueryResponse):
    result: Optional[Union[PoolsRanking, EraMismatch, QueryUnavailableInCurrentEra]]


class ProposedProtocolParametersResponse(QueryResponse):
    result: Optional[
        Union[
            Dict[str, ProtocolParametersShelley],
            Dict[str, ProtocolParametersAlonzo],
            Dict[str, ProtocolParametersBabbage],
            EraMismatch,
            QueryUnavailableInCurrentEra,
        ]
    ]


class RewardsProvenanceResponse(QueryResponse):
    result: Optional[
        Union[RewardsProvenance, EraMismatch, QueryUnavailableInCurrentEra]
    ]


class RewardsProvenanceNewResponse(QueryResponse):
    result: Optional[
        Union[RewardsProvenanceNew, EraMismatch, QueryUnavailableInCurrentEra]
    ]


class StakeDistributionResponse(QueryResponse):
    result: Optional[Union[PoolDistribution, EraMismatch, QueryUnavailableInCurrentEra]]


class SystemStartResponse(QueryResponse):
    result: Optional[Union[UtcTime, EraMismatch, QueryUnavailableInCurrentEra]]


class UtxoResponse(QueryResponse):
    result: Optional[Union[Utxo, EraMismatch, QueryUnavailableInCurrentEra]]


Response.update_forward_refs()
