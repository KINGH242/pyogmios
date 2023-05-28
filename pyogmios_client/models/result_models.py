from typing import List, Union, Optional, Dict

from pydantic import Extra, Field

from pyogmios_client.models import (
    TipOrOrigin,
    TxId,
    AcquireFailureDetails,
    PointOrOrigin,
    Block,
    SubmitTxErrorMalformedScriptWitnesses,
    SubmitTxErrorMalformedReferenceScripts,
    SubmitTxErrorTotalCollateralMismatch,
    SubmitTxErrorMirNegativeTransfer,
    SubmitTxErrorExtraScriptWitnesses,
    SubmitTxErrorCollectErrors,
    SubmitTxErrorValidationTagMismatch,
    SubmitTxErrorOutsideForecast,
    SubmitTxErrorExecutionUnitsTooLarge,
    SubmitTxErrorTooManyCollateralInputs,
    SubmitTxErrorCollateralHasNonAdaAssets,
    SubmitTxErrorCollateralIsScript,
    SubmitTxErrorCollateralTooSmall,
    SubmitTxErrorMissingCollateralInputs,
    SubmitTxErrorMissingDatumHashesForInputs,
    SubmitTxErrorExtraRedeemers,
    SubmitTxErrorUnspendableScriptInputs,
    SubmitTxErrorMissingRequiredSignatures,
    SubmitTxErrorExtraDataMismatch,
    SubmitTxErrorUnspendableDatums,
    SubmitTxErrorMissingRequiredDatums,
    SubmitTxErrorMissingRequiredRedeemers,
    SubmitTxErrorProtocolVersionCannotFollow,
    SubmitTxErrorUpdateWrongEpoch,
    SubmitTxErrorNonGenesisVoters,
    SubmitTxErrorDuplicateGenesisVrf,
    SubmitTxErrorMirProducesNegativeUpdate,
    SubmitTxErrorMirNegativeTransferNotCurrentlyAllowed,
    SubmitTxErrorMirTransferNotCurrentlyAllowed,
    SubmitTxErrorTooLateForMir,
    SubmitTxErrorInsufficientFundsForMir,
    SubmitTxErrorAlreadyDelegating,
    SubmitTxErrorUnknownGenesisKey,
    SubmitTxErrorWrongCertificateType,
    SubmitTxErrorRewardAccountNotEmpty,
    SubmitTxErrorRewardAccountNotExisting,
    SubmitTxErrorStakeKeyNotRegistered,
    SubmitTxErrorPoolMetadataHashTooBig,
    SubmitTxErrorPoolCostTooSmall,
    SubmitTxErrorStakeKeyAlreadyRegistered,
    SubmitTxErrorWrongPoolCertificate,
    SubmitTxErrorWrongRetirementEpoch,
    SubmitTxErrorStakePoolNotRegistered,
    SubmitTxErrorUnknownOrIncompleteWithdrawals,
    SubmitTxErrorDelegateNotRegistered,
    SubmitTxErrorTriesToForgeAda,
    SubmitTxErrorAddressAttributesTooLarge,
    SubmitTxErrorTooManyAssetsInOutput,
    SubmitTxErrorOutputTooSmall,
    SubmitTxErrorNetworkMismatch,
    SubmitTxErrorValueNotConserved,
    SubmitTxErrorFeeTooSmall,
    SubmitTxErrorInvalidMetadata,
    SubmitTxErrorMissingAtLeastOneInputUtxo,
    SubmitTxErrorTxTooLarge,
    SubmitTxErrorOutsideOfValidityInterval,
    SubmitTxErrorExpiredUtxo,
    SubmitTxErrorBadInputs,
    SubmitTxErrorTxMetadataHashMismatch,
    SubmitTxErrorMissingTxMetadataHash,
    SubmitTxErrorMissingTxMetadata,
    SubmitTxErrorInsufficientGenesisSignatures,
    SubmitTxErrorScriptWitnessNotValidating,
    SubmitTxErrorMissingScriptWitnesses,
    SubmitTxErrorMissingVkWitnesses,
    SubmitTxErrorInvalidWitnesses,
    EraMismatch,
    Slot,
    ExUnits,
)
from pyogmios_client.models.base_model import BaseModel


class AcquireFailure(BaseModel):
    class Config:
        extra = Extra.forbid

    failure: AcquireFailureDetails


class AcquireSuccess(BaseModel):
    class Config:
        extra = Extra.forbid

    point: PointOrOrigin


class AwaitAcquired(BaseModel):
    class Config:
        extra = Extra.forbid

    slot: Slot


class EvaluationResult(BaseModel):
    class Config:
        extra = Extra.forbid

    EvaluationResult: Dict[str, ExUnits]


class IntersectionFound(BaseModel):
    class Config:
        extra = Extra.forbid

    point: PointOrOrigin
    tip: TipOrOrigin


class IntersectionNotFound(BaseModel):
    class Config:
        extra = Extra.forbid

    tip: TipOrOrigin


class RollBackward(BaseModel):
    class Config:
        extra = Extra.forbid

    point: PointOrOrigin
    tip: TipOrOrigin


class RollForward(BaseModel):
    class Config:
        extra = Extra.forbid

    block: Block
    tip: TipOrOrigin


class SubmitSuccess(BaseModel):
    class Config:
        extra = Extra.forbid

    txId: TxId


class SubmitTxError(BaseModel):
    __root__: List[
        Union[
            EraMismatch,
            SubmitTxErrorInvalidWitnesses,
            SubmitTxErrorMissingVkWitnesses,
            SubmitTxErrorMissingScriptWitnesses,
            SubmitTxErrorScriptWitnessNotValidating,
            SubmitTxErrorInsufficientGenesisSignatures,
            SubmitTxErrorMissingTxMetadata,
            SubmitTxErrorMissingTxMetadataHash,
            SubmitTxErrorTxMetadataHashMismatch,
            SubmitTxErrorBadInputs,
            SubmitTxErrorExpiredUtxo,
            SubmitTxErrorOutsideOfValidityInterval,
            SubmitTxErrorTxTooLarge,
            SubmitTxErrorMissingAtLeastOneInputUtxo,
            SubmitTxErrorInvalidMetadata,
            SubmitTxErrorFeeTooSmall,
            SubmitTxErrorValueNotConserved,
            SubmitTxErrorNetworkMismatch,
            SubmitTxErrorOutputTooSmall,
            SubmitTxErrorTooManyAssetsInOutput,
            SubmitTxErrorAddressAttributesTooLarge,
            SubmitTxErrorTriesToForgeAda,
            SubmitTxErrorDelegateNotRegistered,
            SubmitTxErrorUnknownOrIncompleteWithdrawals,
            SubmitTxErrorStakePoolNotRegistered,
            SubmitTxErrorWrongRetirementEpoch,
            SubmitTxErrorWrongPoolCertificate,
            SubmitTxErrorStakeKeyAlreadyRegistered,
            SubmitTxErrorPoolCostTooSmall,
            SubmitTxErrorPoolMetadataHashTooBig,
            SubmitTxErrorStakeKeyNotRegistered,
            SubmitTxErrorRewardAccountNotExisting,
            SubmitTxErrorRewardAccountNotEmpty,
            SubmitTxErrorWrongCertificateType,
            SubmitTxErrorUnknownGenesisKey,
            SubmitTxErrorAlreadyDelegating,
            SubmitTxErrorInsufficientFundsForMir,
            SubmitTxErrorTooLateForMir,
            SubmitTxErrorMirTransferNotCurrentlyAllowed,
            SubmitTxErrorMirNegativeTransferNotCurrentlyAllowed,
            SubmitTxErrorMirProducesNegativeUpdate,
            SubmitTxErrorDuplicateGenesisVrf,
            SubmitTxErrorNonGenesisVoters,
            SubmitTxErrorUpdateWrongEpoch,
            SubmitTxErrorProtocolVersionCannotFollow,
            SubmitTxErrorMissingRequiredRedeemers,
            SubmitTxErrorMissingRequiredDatums,
            SubmitTxErrorUnspendableDatums,
            SubmitTxErrorExtraDataMismatch,
            SubmitTxErrorMissingRequiredSignatures,
            SubmitTxErrorUnspendableScriptInputs,
            SubmitTxErrorExtraRedeemers,
            SubmitTxErrorMissingDatumHashesForInputs,
            SubmitTxErrorMissingCollateralInputs,
            SubmitTxErrorCollateralTooSmall,
            SubmitTxErrorCollateralIsScript,
            SubmitTxErrorCollateralHasNonAdaAssets,
            SubmitTxErrorTooManyCollateralInputs,
            SubmitTxErrorExecutionUnitsTooLarge,
            SubmitTxErrorOutsideForecast,
            SubmitTxErrorValidationTagMismatch,
            SubmitTxErrorCollectErrors,
            SubmitTxErrorExtraScriptWitnesses,
            SubmitTxErrorMirNegativeTransfer,
            SubmitTxErrorTotalCollateralMismatch,
            SubmitTxErrorMalformedReferenceScripts,
            SubmitTxErrorMalformedScriptWitnesses,
        ]
    ]


class Result(BaseModel):
    class Config:
        extra = Extra.forbid

    acquire_failure: Optional[AcquireFailure] = Field(..., alias="AcquireFailure")
    acquire_success: Optional[AcquireSuccess] = Field(..., alias="Released")
    await_acquired: Optional[AwaitAcquired] = Field(..., alias="AwaitAcquired")
    evaluation_result: Optional[EvaluationResult] = Field(..., alias="EvaluationResult")
    intersection_found: Optional[IntersectionFound] = Field(
        ..., alias="IntersectionFound"
    )
    intersection_not_found: Optional[IntersectionNotFound] = Field(
        ..., alias="IntersectionNotFound"
    )
    released: Optional[str] = Field(..., alias="Released")
    roll_backward: Optional[RollBackward] = Field(..., alias="RollBackward")
    roll_forward: Optional[RollForward] = Field(..., alias="RollForward")
    submit_success: Optional[SubmitSuccess] = Field(..., alias="SubmitSuccess")
    submit_tx_error: Optional[SubmitTxError] = Field(..., alias="SubmitTxError")
