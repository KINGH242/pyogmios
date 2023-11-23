from __future__ import annotations

from typing import Optional, Any, Dict, Union, List

from pydantic import Field, ConfigDict

from pyogmios_client.enums import MethodName, Type, Version, ServiceName
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
    fault: Optional[Dict[str, Any]] = None
    reflection: Optional[Any] = Field(
        None,
        description="An arbitrary JSON value that will be mirrored back in the response.",
    )
    result: Optional[Any] = None

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class SubmitSuccess(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
    )

    txId: TxId


class SubmitTxResponseSubmitSuccess(BaseModel):
    SubmitSuccess: SubmitSuccess


class SubmitTxResponseSubmitFail(BaseModel):
    SubmitFail: SubmitTxError


class SubmitTxResponse(BaseModel):
    methodname: MethodName = MethodName.SUBMIT_TX
    result: Union[SubmitTxResponseSubmitSuccess, SubmitTxResponseSubmitFail]
    reflection: Optional[Dict[str, Any]] = None


class EvaluateTxResponse(BaseModel):
    methodname: MethodName = MethodName.EVALUATE_TX
    result: Union[EvaluationResult, EvaluationFailure]
    reflection: Optional[Dict[str, Any]] = None


class AwaitAcquireResponse(BaseModel):
    methodname: MethodName = MethodName.AWAIT_ACQUIRE
    result: AwaitAcquiredResult
    reflection: Optional[Dict[str, Any]] = None


class HasTxResponse(BaseModel):
    methodname: MethodName = MethodName.HAS_TX
    result: bool
    reflection: Optional[Dict[str, Any]] = None


class NextTxResponse(BaseModel):
    methodname: MethodName = MethodName.NEXT_TX
    result: Union[TxId, TxAlonzo, TxBabbage, Null]
    reflection: Optional[Dict[str, Any]] = None


class ReleaseMempoolResponse(BaseModel):
    methodname: MethodName = MethodName.RELEASE_MEMPOOL
    result: str
    reflection: Optional[Dict[str, Any]] = None


class SizeAndCapacityResponse(BaseModel):
    methodname: MethodName = MethodName.SIZE_AND_CAPACITY
    result: MempoolSizeAndCapacity
    reflection: Optional[Dict[str, Any]] = None


class QueryResponseReflection(BaseModel):
    requestId: Optional[str] = None

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class QueryResponse(Response):
    methodname: MethodName = MethodName.QUERY
    reflection: Optional[QueryResponseReflection] = None
    result: Optional[Any] = None

    @staticmethod
    def from_base_response(
        reflection: Optional[Any] = None,
        result: Optional[Any] = None,
    ) -> QueryResponse:
        return QueryResponse(
            type=Type.JSONWSP_RESPONSE,
            version=Version.v1_0,
            servicename=ServiceName.OGMIOS,
            reflection=reflection,
            result=result,
        )


class FindIntersectResponse(QueryResponse):
    methodname: MethodName = MethodName.FIND_INTERSECT
    result: FindIntersectResult

    class Config:
        populate_by_name = True


class QueryResponseBlockHeight(QueryResponse):
    result: Union[BlockNoOrOrigin, QueryUnavailableInCurrentEra]


class RequestNextResponse(QueryResponse):
    result: Union[RollForwardResult, RollBackwardResult]


class ReleaseResponse(QueryResponse):
    methodname: MethodName = MethodName.RELEASE
    result: ReleaseResponseResult


class AcquireResponse(QueryResponse):
    methodname: MethodName = MethodName.ACQUIRE
    result: Union[AcquireSuccessResult, AcquireFailureResult]


class ChainTipResponse(QueryResponse):
    result: Optional[Union[PointOrOrigin, QueryUnavailableInCurrentEra]] = None


class CurrentEpochResponse(QueryResponse):
    result: Optional[
        Union[Epoch, EraMismatchResult, QueryUnavailableInCurrentEra]
    ] = None


class CurrentProtocolParametersResponse(QueryResponse):
    result: Optional[
        Union[
            ProtocolParametersShelley,
            ProtocolParametersAlonzo,
            ProtocolParametersBabbage,
            EraMismatchResult,
            QueryUnavailableInCurrentEra,
        ]
    ] = None


class DelegationsAndRewardsResponse(QueryResponse):
    result: Optional[
        Union[
            DelegationsAndRewardsByAccounts,
            EraMismatchResult,
            QueryUnavailableInCurrentEra,
        ]
    ] = None


class EraStartResponse(QueryResponse):
    result: Optional[Union[Bound, QueryUnavailableInCurrentEra]] = None


class EraSummariesResponse(QueryResponse):
    result: Optional[Union[List[EraSummary], QueryUnavailableInCurrentEra]] = None


class GenesisConfigResponse(QueryResponse):
    result: Optional[
        Union[
            GenesisByron,
            GenesisShelley,
            GenesisAlonzo,
            EraMismatch,
            QueryUnavailableInCurrentEra,
        ]
    ] = None


class LedgerTipResponse(QueryResponse):
    result: Optional[
        Union[PointOrOrigin, EraMismatch, QueryUnavailableInCurrentEra]
    ] = None


class NonMyopicMemberRewardsResponse(QueryResponse):
    result: Optional[
        Union[NonMyopicMemberRewards, EraMismatch, QueryUnavailableInCurrentEra]
    ] = None


class PoolIdsResponse(QueryResponse):
    result: Optional[
        Union[List[PoolId], EraMismatch, QueryUnavailableInCurrentEra]
    ] = None


class PoolParametersResponse(QueryResponse):
    result: Optional[
        Union[Dict[str, PoolParameters], EraMismatch, QueryUnavailableInCurrentEra]
    ] = None


class PoolsRankingResponse(QueryResponse):
    result: Optional[
        Union[PoolsRanking, EraMismatch, QueryUnavailableInCurrentEra]
    ] = None


class ProposedProtocolParametersResponse(QueryResponse):
    result: Optional[
        Union[
            Dict[str, ProtocolParametersShelley],
            Dict[str, ProtocolParametersAlonzo],
            Dict[str, ProtocolParametersBabbage],
            EraMismatch,
            QueryUnavailableInCurrentEra,
        ]
    ] = None


class RewardsProvenanceResponse(QueryResponse):
    result: Optional[
        Union[RewardsProvenance, EraMismatch, QueryUnavailableInCurrentEra]
    ] = None


class RewardsProvenanceNewResponse(QueryResponse):
    result: Optional[
        Union[RewardsProvenanceNew, EraMismatch, QueryUnavailableInCurrentEra]
    ] = None


class StakeDistributionResponse(QueryResponse):
    result: Optional[
        Union[PoolDistribution, EraMismatch, QueryUnavailableInCurrentEra]
    ] = None


class SystemStartResponse(QueryResponse):
    result: Optional[Union[UtcTime, EraMismatch, QueryUnavailableInCurrentEra]] = None


class UtxoResponse(QueryResponse):
    result: Optional[Union[Utxo, EraMismatch, QueryUnavailableInCurrentEra]] = None


Response.model_rebuild()
