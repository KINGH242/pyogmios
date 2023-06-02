from typing import List, Union, Optional, Dict


from pyogmios_client.enums import AcquireFailureDetails
from pyogmios_client.models import (
    SubmitTxErrorUnspendableDatums,
    SubmitTxErrorCollectErrors,
    SubmitTxErrorExecutionUnitsTooLarge,
    SubmitTxErrorCollateralHasNonAdaAssets,
    SubmitTxErrorCollateralIsScript,
    SubmitTxErrorMissingDatumHashesForInputs,
    SubmitTxErrorExtraRedeemers,
    SubmitTxErrorUnspendableScriptInputs,
    SubmitTxErrorMissingRequiredRedeemers,
    SubmitTxErrorUpdateWrongEpoch,
    SubmitTxErrorWrongPoolCertificate,
    SubmitTxErrorTooManyAssetsInOutput,
    SubmitTxErrorOutputTooSmall,
    SubmitTxErrorNetworkMismatch,
    SubmitTxErrorValueNotConserved,
    SubmitTxErrorOutsideOfValidityInterval,
    SubmitTxErrorBadInputs,
    SubmitTxErrorInvalidWitnesses,
    EraMismatch,
    PointOrOrigin,
    Slot,
    ExUnits,
    TipOrOrigin,
    Block,
    TxId,
    SubmitTxErrorMissingVkWitnesses,
    SubmitTxErrorMissingScriptWitnesses,
    SubmitTxErrorScriptWitnessNotValidating,
    SubmitTxErrorInsufficientGenesisSignatures,
    SubmitTxErrorMirNegativeTransferNotCurrentlyAllowed,
    SubmitTxErrorMissingTxMetadata,
    SubmitTxErrorMissingTxMetadataHash,
    SubmitTxErrorMirTransferNotCurrentlyAllowed,
    SubmitTxErrorTxMetadataHashMismatch,
    SubmitTxErrorExpiredUtxo,
    SubmitTxErrorTxTooLarge,
    SubmitTxErrorMissingAtLeastOneInputUtxo,
    SubmitTxErrorInvalidMetadata,
    SubmitTxErrorFeeTooSmall,
    SubmitTxErrorAddressAttributesTooLarge,
    SubmitTxErrorTriesToForgeAda,
    SubmitTxErrorDelegateNotRegistered,
    SubmitTxErrorUnknownOrIncompleteWithdrawals,
    SubmitTxErrorStakePoolNotRegistered,
    SubmitTxErrorWrongRetirementEpoch,
    SubmitTxErrorStakeKeyAlreadyRegistered,
    SubmitTxErrorPoolCostTooSmall,
    SubmitTxErrorPoolMetadataHashTooBig,
    SubmitTxErrorStakeKeyNotRegistered,
    SubmitTxErrorRewardAccountNotExisting,
    SubmitTxErrorWrongCertificateType,
    SubmitTxErrorRewardAccountNotEmpty,
    SubmitTxErrorUnknownGenesisKey,
    SubmitTxErrorAlreadyDelegating,
    SubmitTxErrorInsufficientFundsForMir,
    SubmitTxErrorTooLateForMir,
    SubmitTxErrorMirProducesNegativeUpdate,
    SubmitTxErrorDuplicateGenesisVrf,
    SubmitTxErrorNonGenesisVoters,
    SubmitTxErrorProtocolVersionCannotFollow,
    SubmitTxErrorMissingRequiredDatums,
    SubmitTxErrorExtraDataMismatch,
    SubmitTxErrorMissingRequiredSignatures,
    SubmitTxErrorMissingCollateralInputs,
    SubmitTxErrorCollateralTooSmall,
    SubmitTxErrorTooManyCollateralInputs,
    SubmitTxErrorValidationTagMismatch,
    SubmitTxErrorOutsideForecast,
    SubmitTxErrorExtraScriptWitnesses,
    SubmitTxErrorMirNegativeTransfer,
    SubmitTxErrorTotalCollateralMismatch,
    SubmitTxErrorMalformedReferenceScripts,
    SubmitTxErrorMalformedScriptWitnesses,
)
from pyogmios_client.models.base_model import BaseModel


class AcquireFailure(BaseModel):
    failure: AcquireFailureDetails


class AcquireSuccess(BaseModel):
    point: PointOrOrigin


class AwaitAcquired(BaseModel):
    slot: Slot


class EvaluationResult(BaseModel):
    EvaluationResult: Dict[str, ExUnits]


class IntersectionFound(BaseModel):
    point: PointOrOrigin
    tip: TipOrOrigin


class IntersectionNotFound(BaseModel):
    tip: TipOrOrigin


class RollBackward(BaseModel):
    point: PointOrOrigin
    tip: TipOrOrigin


class RollForward(BaseModel):
    block: Block
    tip: TipOrOrigin


class SubmitSuccess(BaseModel):
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
    AcquireFailure: Optional[AcquireFailure]
    AcquireSuccess: Optional[AcquireSuccess]
    AwaitAcquired: Optional[AwaitAcquired]
    EvaluationResult: Optional[EvaluationResult]
    IntersectionFound: Optional[IntersectionFound]
    IntersectionNotFound: Optional[IntersectionNotFound]
    Released: Optional[str]
    RollBackward: Optional[RollBackward]
    RollForward: Optional[RollForward]
    SubmitSuccess: Optional[SubmitSuccess]
    SubmitTxError: Optional[SubmitTxError]
