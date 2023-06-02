from __future__ import annotations

from datetime import datetime
from enum import Enum
from types import UnionType
from typing import Optional, Dict, List, Union

from pydantic import conint, Field, Extra, constr, confloat, AnyUrl

from pyogmios_client.enums import (
    RewardPot,
    NonceEnum,
    Network,
    InputSource,
    Language,
    InvalidEntityType,
    InvalidEntityEntity,
)
from pyogmios_client.models.base_model import BaseModel

Slot = int

# Origin = 'origin'
class Origin(BaseModel):
    __root__: str = "origin"


BlockNo = int

Metadatum: UnionType = int | str | bytes | List | Dict


class Address(BaseModel):
    __root__: constr(regex=r"[1-9A-HJ-NP-Za-km-z]*") = Field(
        ...,
        description="A Cardano address (either legacy format or new format).",
        examples=[
            "addr1q9d34spgg2kdy47n82e7x9pdd6vql6d2engxmpj20jmhuc2047yqd4xnh7u6u5jp4t0q3fkxzckph4tgnzvamlu7k5psuahzcp",
            "DdzFFzCqrht8mbSTZHqpM2u4HeND2mdspsaBhdQ1BowPJBMzbDeBMeKgqdoKqo1D4sdPusEdZJVrFJRBBxX1jUEofNDYCJSZLg8MkyCE",
        ],
    )


class AddressAttributes(BaseModel):
    __root__: str = Field(
        ...,
        description="Extra attributes carried by Byron addresses (network magic and/or HD payload).",
    )


class AssetQuantity(BaseModel):
    __root__: int = Field(
        ..., description="A number of asset, can be negative went burning assets."
    )


class BlockNo(BaseModel):
    __root__: conint(ge=0, le=18446744073709552999) = Field(
        ..., description="A block number, the i-th block to be minted is number i."
    )


class BlockSize(BaseModel):
    __root__: conint(ge=0, le=18446744073709552999) = Field(
        ..., description="The size of the block in bytes."
    )


class StakeDelegation(BaseModel):
    delegator: DigestBlake2bCredential
    delegatee: PoolId


class StakeDelegationCertificate(BaseModel):
    stakeDelegation: StakeDelegation


class StakeKeyRegistrationCertificate(BaseModel):
    stakeKeyRegistration: DigestBlake2bCredential


class StakeKeyDeregistrationCertificate(BaseModel):
    stakeKeyDeregistration: DigestBlake2bCredential


class PoolRegistrationCertificate(BaseModel):
    poolRegistration: PoolParameters


class PoolRetirement(BaseModel):
    retirementEpoch: Epoch
    poolId: PoolId


class PoolRetirementCertificate(BaseModel):
    poolRetirement: PoolRetirement


class GenesisDelegation(BaseModel):
    delegateKeyHash: DigestBlake2bVerificationKey
    verificationKeyHash: DigestBlake2bVerificationKey
    vrfVerificationKeyHash: DigestBlake2bVrfVerificationKey


class GenesisDelegationCertificate(BaseModel):
    genesisDelegation: GenesisDelegation


class MoveInstantaneousRewards(BaseModel):
    rewards: Optional[Rewards] = None
    value: Optional[Lovelace] = None
    pot: RewardPot


class MoveInstantaneousRewardsCertificate(BaseModel):
    moveInstantaneousRewards: MoveInstantaneousRewards


Certificate = (
    StakeDelegationCertificate
    | StakeKeyRegistrationCertificate
    | StakeKeyDeregistrationCertificate
    | PoolRegistrationCertificate
    | PoolRetirementCertificate
    | GenesisDelegationCertificate
    | MoveInstantaneousRewardsCertificate
)


class CertifiedVrf(BaseModel):
    class Config:
        extra = Extra.forbid

    proof: Optional[VrfProof] = None
    output: Optional[VrfOutput] = None


class ChainCode(BaseModel):
    __root__: str = Field(
        ..., description="An Ed25519-BIP32 chain-code for key deriviation."
    )


class CostModel(BaseModel):
    __root__: Optional[Dict[str, Int64]] = None


class CostModels(BaseModel):
    __root__: Optional[Dict[str, CostModel]] = None


class Datum(BaseModel):
    __root__: str


class DigestBlake2bAuxiliaryDataBody(BaseModel):
    __root__: constr(min_length=64, max_length=64) = Field(
        ...,
        description="A Blake2b 32-byte digest of an 'AuxiliaryDataBody', serialised as CBOR.",
        examples=["c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d"],
    )


class DigestBlake2bBlockBody(BaseModel):
    __root__: constr(min_length=64, max_length=64) = Field(
        ...,
        description="A Blake2b 32-byte digest of an era-independent block body.",
        examples=["c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d"],
    )


class HeaderEnum(Enum):
    genesis = "genesis"


class DigestBlake2bBlockHeader(BaseModel):
    __root__: Union[constr(min_length=64, max_length=64), HeaderEnum]


class DigestBlake2bCredential(BaseModel):
    __root__: constr(min_length=56, max_length=56) = Field(
        ...,
        description="A Blake2b 28-byte digest of a verification key or a script.",
        examples=["90181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d3"],
    )


class DigestBlake2bDatum(BaseModel):
    __root__: constr(min_length=64, max_length=64) = Field(
        ...,
        description="A Blake2b 32-byte digest of a serialized datum, CBOR-encoded.",
        examples=["c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d"],
    )


class DigestBlake2bMerkleRoot(BaseModel):
    __root__: constr(min_length=64, max_length=64) = Field(
        ...,
        description="A Blake2b 32-byte digest of a Merkle tree (or all block's transactions) root hash.",
        examples=["c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d"],
    )


class DigestBlake2bNonce(BaseModel):
    __root__: constr(min_length=64, max_length=64) = Field(
        ...,
        description="A Blake2b 32-byte digest of some arbitrary to make a nonce.",
        examples=["c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d"],
    )


class DigestBlake2bPoolMetadata(BaseModel):
    __root__: str = Field(
        ...,
        description="A Blake2b 32-byte digest of stake pool (canonical) JSON metadata.",
        examples=["c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d"],
    )


class DigestBlake2bScript(BaseModel):
    __root__: constr(min_length=56, max_length=56) = Field(
        ...,
        description="A Blake2b 32-byte digest of a phase-1 or phase-2 script, CBOR-encoded.",
        examples=["90181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d3"],
    )


class DigestBlake2bScriptIntegrity(BaseModel):
    __root__: constr(min_length=64, max_length=64) = Field(
        ...,
        description="A Blake2b 32-byte digest of a script-integrity hash (i.e redeemers, datums and cost model, CBOR-encoded).",
        examples=["c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d"],
    )


class DigestBlake2bVerificationKey(BaseModel):
    __root__: constr(min_length=56, max_length=56) = Field(
        ...,
        description="A Blake2b 28-byte digest of an Ed25519 verification key.",
        examples=["90181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d3"],
    )


class DigestBlake2bVrfVerificationKey(BaseModel):
    __root__: constr(min_length=64, max_length=64) = Field(
        ...,
        description="A Blake2b 32-byte digest of a VRF verification key.",
        examples=["c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d"],
    )


class HeaderHash(BaseModel):
    __root__: DigestBlake2bBlockHeader


class Nonce(BaseModel):
    __root__: NonceEnum | DigestBlake2bNonce


class DlgPayload(BaseModel):
    __root__: constr(min_length=64, max_length=64) = Field(
        ...,
        description="A Blake2b 32-byte digest of a Byron delegation payload, CBOR-encoded.",
        examples=["c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d"],
    )


class Epoch(BaseModel):
    __root__: conint(ge=0, le=18446744073709552000) = Field(
        ..., description="An epoch number or length."
    )


class ExUnits(BaseModel):
    class Config:
        extra = Extra.forbid

    memory: UInt64
    steps: UInt64


class GenesisVerificationKey(BaseModel):
    __root__: constr(min_length=128, max_length=128) = Field(
        ...,
        description="An Ed25519-BIP32 Byron genesis delegate verification key with chain-code.",
    )


class IssuerVrfVerificationKey(BaseModel):
    __root__: str = Field(..., description="A key identifying a block issuer.")


class IssuerSignature(BaseModel):
    __root__: str = Field(
        ...,
        description="Signature proving a block was issued by a given issuer VRF key.",
    )


class Int64(BaseModel):
    __root__: conint(ge=-9223372036854775808, le=9223372036854775807)


class KesVerificationKey(BaseModel):
    __root__: str


class Lovelace(BaseModel):
    __root__: int = Field(
        ..., description="A number of lovelace, possibly large when summed up."
    )


class LovelaceDelta(BaseModel):
    __root__: conint(ge=-9223372036854775808, le=9223372036854775807) = Field(
        ...,
        description="An amount, possibly negative, in Lovelace (1e6 Lovelace = 1 Ada).",
    )


class MempoolSizeAndCapacity(BaseModel):
    class Config:
        extra = Extra.forbid

    capacity: UInt32
    currentSize: UInt32
    numberOfTxs: UInt32


class NetworkMagic(BaseModel):
    __root__: conint(ge=0, le=4294967296) = Field(
        ...,
        description="A magic number for telling networks apart. (e.g. 764824073)",
        examples=[764824073],
    )


class NonMyopicMemberRewards(BaseModel):
    __root__: Optional[Dict[str, Dict[str, confloat(ge=0.0)]]] = None


class Null(BaseModel):
    __root__: None


class NullableRatio(BaseModel):
    __root__: Ratio | Null


class NullableUInt64(BaseModel):
    __root__: UInt64 | Null


class ProtocolMagicId(BaseModel):
    __root__: conint(ge=0, le=4294967295) = Field(..., examples=[764824073])


class ProtocolVersion(BaseModel):
    class Config:
        extra = Extra.forbid

    major: UInt32
    minor: UInt32
    patch: Optional[UInt32] = None


class PoolId(BaseModel):
    __root__: constr(regex=r"^pool1[0-9a-z]*$") = Field(
        ...,
        description="A Blake2b 32-byte digest of a pool's verification key.",
        examples=[
            "pool1qqqqpanw9zc0rzh0yp247nzf2s35uvnsm7aaesfl2nnejaev0uc",
            "pool1qqqqqdk4zhsjuxxd8jyvwncf5eucfskz0xjjj64fdmlgj735lr9",
        ],
    )


class Prices(BaseModel):
    class Config:
        extra = Extra.forbid

    memory: Ratio
    steps: Ratio


class Ratio(BaseModel):
    __root__: constr(regex=r"^-?[0-9]+/[0-9]+$") = Field(
        ...,
        description="A ratio of two integers, to express exact fractions.",
        examples=["2/3", "7/8"],
    )


class Redeemer(BaseModel):
    class Config:
        extra = Extra.forbid

    redeemer: RedeemerData
    executionUnits: ExUnits


class RedeemerData(BaseModel):
    __root__: str = Field(..., description="Plutus data, CBOR-serialised.")


class RedeemerPointer(BaseModel):
    __root__: constr(regex=r"^(spend|mint|certificate|withdrawal):[0-9]+$")


class RelativeTime(BaseModel):
    __root__: confloat(ge=0.0) = Field(
        ...,
        description="A time in seconds relative to another one (typically, system start or era start). Starting from v5.5.4, this can be a floating number. Before v5.5.4, the floating value would be rounded to the nearest second.",
    )


class Rewards(BaseModel):
    __root__: Optional[Dict[str, LovelaceDelta]] = None


class RewardAccount(BaseModel):
    __root__: constr(regex=r"^stake(_test)?1[0-9a-z]+$") = Field(
        ...,
        description="A reward account, also known as 'stake address'.",
        examples=["stake1ux7pt9adw8z46tgqn2f8fvurrhk325gcm4mf75mkmmxpx6gae9mzv"],
    )


class SoftwareVersion(BaseModel):
    class Config:
        extra = Extra.forbid

    appName: str
    number: UInt32


class StakeAddress(BaseModel):
    __root__: constr(regex=r"^(stake|stake_test)1[0-9a-z]*$") = Field(
        ...,
        description="A stake address (a.k.a reward account)",
        examples=["stake179kzq4qulejydh045yzxwk4ksx780khkl4gdve9kzwd9vjcek9u8h"],
    )


class Signature(BaseModel):
    __root__: str = Field(
        ...,
        description="A signature coming from an Ed25519 or Ed25519-BIP32 signing key.",
    )


class SoftForkRule(BaseModel):
    class Config:
        extra = Extra.forbid

    initThreshold: NullableRatio
    minThreshold: NullableRatio
    decrementThreshold: NullableRatio


class TxFeePolicy(BaseModel):
    class Config:
        extra = Extra.forbid

    coefficient: Ratio
    constant: float


class TxId(BaseModel):
    __root__: constr(min_length=64, max_length=64) = Field(
        ..., description="A Blake2b 32-byte digest of a transaction body, CBOR-encoded."
    )


class UInt32(BaseModel):
    __root__: conint(ge=0, le=4294967295)


class UInt64(BaseModel):
    __root__: conint(ge=0, le=18446744073709552999)


class UpdatePayload(BaseModel):
    __root__: constr(min_length=64, max_length=64) = Field(
        ...,
        description="A Blake2b 32-byte digest of a Byron update payload, CBOR-encoded.",
        examples=["c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d"],
    )


class UtcTime(BaseModel):
    __root__: datetime


class Value(BaseModel):
    class Config:
        extra = Extra.forbid

    coins: Lovelace
    assets: Optional[Dict[str, AssetQuantity]] = None


class VerificationKey(BaseModel):
    __root__: constr(min_length=64, max_length=64) = Field(
        ..., description="An Ed25519 verification key."
    )


class VrfOutput(BaseModel):
    __root__: str


class VrfProof(BaseModel):
    __root__: str


class Withdrawals(BaseModel):
    __root__: Optional[Dict[str, Lovelace]] = None


class WitnessHash(BaseModel):
    __root__: constr(min_length=64, max_length=64) = Field(
        ...,
        description="A Blake2b 32-byte digest of a Byron transaction witness set, CBOR-encoded.",
        examples=["c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d"],
    )


class ScriptNative(BaseModel):
    __root__: DigestBlake2bVerificationKey | Any | All | NOf | ExpiresAt | StartsAt = Field(
        ...,
        description="A phase-1 monetary script. Timelocks constraints are only supported since Allegra.",
        examples=[
            "3c07030e36bfff7cd2f004356ef320f3fe3c07030e7cd2f004356437",
            {
                "all": [
                    "ec09e5293d384637cd2f004356ef320f3fe3c07030e36bfffe67e2e2",
                    "3c07030e36bfff7cd2f004356ef320f3fe3c07030e7cd2f004356437",
                ]
            },
        ],
    )


class ScriptPlutus(BaseModel):
    __root__: str = Field(
        ...,
        description="A phase-2 Plutus script; or said differently, a serialized Plutus-core program.",
    )


class All(BaseModel):
    all: List[ScriptNative]


class Any(BaseModel):
    any: List[ScriptNative]


class NOf(BaseModel):
    __root__: Dict[str, List[ScriptNative]]


class ExpiresAt(BaseModel):
    expires_at: Slot


class StartsAt(BaseModel):
    starts_at: Slot


class Native(BaseModel):
    native: ScriptNative


class PlutusV1(BaseModel):
    plutus_v1: ScriptPlutus = Field(..., alias="plutus:v1")


class PlutusV2(BaseModel):
    plutus_v2: ScriptPlutus = Field(..., alias="plutus:v2")


Script = Native | PlutusV1 | PlutusV2


class PoolMetadata(BaseModel):
    hash: DigestBlake2bPoolMetadata
    url: AnyUrl


class PoolParameters(BaseModel):
    owners: List[DigestBlake2bVerificationKey]
    cost: Lovelace
    margin: Ratio
    pledge: Lovelace
    vrf: DigestBlake2bVrfVerificationKey
    metadata: Null | PoolMetadata
    id: PoolId
    relays: List[Relay]
    rewardAccount: RewardAccount


class OpCert(BaseModel):
    count: Optional[UInt64] = None
    sigma: Optional[Signature] = None
    kesPeriod: Optional[UInt64] = None
    hotVk: Optional[KesVerificationKey] = None


class ByAddress(BaseModel):
    ipv4: str | Null
    ipv6: str | Null
    port: conint(ge=0, le=65535) | Null


class ByName(BaseModel):
    hostname: str
    port: conint(ge=0, le=65535) | Null


Relay = ByAddress | ByName


class DlgCertificate(BaseModel):
    class Config:
        extra = Extra.forbid

    epoch: Epoch
    issuerVk: GenesisVerificationKey
    delegateVk: GenesisVerificationKey
    signature: IssuerSignature


class GenesisByron(BaseModel):
    class Config:
        extra = Extra.forbid

    genesisKeyHashes: List[DigestBlake2bVerificationKey]
    genesisDelegations: Dict[str, DlgCertificate]
    systemStart: UtcTime
    initialFunds: Dict[str, Lovelace]
    initialCoinOffering: Dict[str, Lovelace]
    securityParameter: UInt64
    networkMagic: NetworkMagic
    protocolParameters: ProtocolParametersByron


class GenesisAlonzo(BaseModel):
    class Config:
        extra = Extra.forbid

    coinsPerUtxoWord: UInt64
    collateralPercentage: UInt64
    costModels: CostModels
    maxCollateralInputs: NullableUInt64
    maxExecutionUnitsPerBlock: ExUnits
    maxExecutionUnitsPerTransaction: ExUnits
    maxValueSize: NullableUInt64
    prices: Prices


class GenesisPools(BaseModel):
    class Config:
        extra = Extra.forbid

    pools: Dict[str, PoolParameters]
    delegators: Dict[str, PoolId]


class ProtocolParametersAlonzo(BaseModel):
    class Config:
        extra = Extra.forbid

    minFeeCoefficient: NullableUInt64
    minFeeConstant: NullableUInt64
    maxBlockBodySize: NullableUInt64
    maxBlockHeaderSize: NullableUInt64
    maxTxSize: NullableUInt64
    stakeKeyDeposit: NullableUInt64
    poolDeposit: NullableUInt64
    poolRetirementEpochBound: NullableUInt64
    desiredNumberOfPools: NullableUInt64
    poolInfluence: NullableRatio
    monetaryExpansion: NullableRatio
    treasuryExpansion: NullableRatio
    decentralizationParameter: NullableRatio
    minPoolCost: NullableUInt64
    coinsPerUtxoWord: NullableUInt64
    maxValueSize: NullableUInt64
    collateralPercentage: NullableUInt64
    maxCollateralInputs: NullableUInt64
    extraEntropy: Nonce | Null
    protocolVersion: ProtocolVersion | Null
    costModels: CostModels | Null
    prices: Prices | Null
    maxExecutionUnitsPerTransaction: ExUnits | Null
    maxExecutionUnitsPerBlock: ExUnits | Null


class ProtocolParametersBabbage(BaseModel):
    class Config:
        extra = Extra.forbid

    minFeeCoefficient: NullableUInt64
    minFeeConstant: NullableUInt64
    maxBlockBodySize: NullableUInt64
    maxBlockHeaderSize: NullableUInt64
    maxTxSize: NullableUInt64
    stakeKeyDeposit: NullableUInt64
    poolDeposit: NullableUInt64
    poolRetirementEpochBound: NullableUInt64
    desiredNumberOfPools: NullableUInt64
    poolInfluence: NullableRatio
    monetaryExpansion: NullableRatio
    treasuryExpansion: NullableRatio
    minPoolCost: NullableUInt64
    coinsPerUtxoByte: NullableUInt64
    maxValueSize: NullableUInt64
    collateralPercentage: NullableUInt64
    maxCollateralInputs: NullableUInt64
    protocolVersion: ProtocolVersion | Null
    costModels: CostModels | Null
    prices: Prices | Null
    maxExecutionUnitsPerTransaction: ExUnits | Null
    maxExecutionUnitsPerBlock: ExUnits | Null


class ProtocolParametersByron(BaseModel):
    class Config:
        extra = Extra.forbid

    heavyDlgThreshold: NullableRatio
    maxBlockSize: NullableUInt64
    maxHeaderSize: NullableUInt64
    maxProposalSize: NullableUInt64
    maxTxSize: NullableUInt64
    mpcThreshold: NullableRatio
    scriptVersion: NullableUInt64
    slotDuration: NullableUInt64
    unlockStakeEpoch: NullableUInt64
    updateProposalThreshold: NullableRatio
    updateProposalTimeToLive: NullableUInt64
    updateVoteThreshold: NullableRatio
    txFeePolicy: TxFeePolicy | Null
    softforkRule: SoftForkRule | Null


class ProtocolParametersShelley(BaseModel):
    class Config:
        extra = Extra.forbid

    minFeeCoefficient: NullableUInt64
    minFeeConstant: NullableUInt64
    maxBlockBodySize: NullableUInt64
    maxBlockHeaderSize: NullableUInt64
    maxTxSize: NullableUInt64
    stakeKeyDeposit: NullableUInt64
    poolDeposit: NullableUInt64
    poolRetirementEpochBound: NullableUInt64
    desiredNumberOfPools: NullableUInt64
    poolInfluence: NullableRatio
    monetaryExpansion: NullableRatio
    treasuryExpansion: NullableRatio
    decentralizationParameter: NullableRatio
    minUtxoValue: NullableUInt64
    minPoolCost: NullableUInt64
    extraEntropy: Nonce | Null
    protocolVersion: ProtocolVersion | Null


class Allegra(BaseModel):
    allegra: BlockAllegra


class Alonzo(BaseModel):
    alonzo: BlockAlonzo


class AuxiliaryData(BaseModel):
    hash: DigestBlake2bAuxiliaryDataBody
    body: AuxiliaryDataBody


class AuxiliaryDataBody(BaseModel):
    blob: Optional[Dict[str, Metadatum]] = None
    scripts: Optional[List[Script]] = None


class Babbage(BaseModel):
    babbage: BlockBabbage


class BlockAllegra(BaseModel):
    body: List[TxAllegra]
    headerHash: HeaderHash
    header: Header


class BlockAlonzo(BaseModel):
    body: List[TxAlonzo]
    headerHash: HeaderHash
    header: Header


class BlockBabbage(BaseModel):
    body: List[TxBabbage]
    headerHash: DigestBlake2bBlockHeader
    header: Header


class BlockMary(BaseModel):
    body: List[TxMary]
    headerHash: HeaderHash
    header: Header


class BlockProof(BaseModel):
    utxo: Utxo
    delegation: DlgPayload
    update: UpdatePayload


class BlockShelley(BaseModel):
    body: List[TxShelley]
    headerHash: DigestBlake2bBlockHeader
    header: Header


class BlockSignature(BaseModel):
    dlgCertificate: DlgCertificate
    signature: IssuerSignature


class Byron(BaseModel):
    byron: BlockByron


class EpochBoundaryBlock(BaseModel):
    hash: DigestBlake2bBlockHeader
    header: EpochBoundaryBlockHeader


class EpochBoundaryBlockHeader(BaseModel):
    blockHeight: BlockNo
    epoch: Epoch
    prevHash: DigestBlake2bBlockHeader


class Header(BaseModel):
    blockHeight: BlockNo
    slot: Slot
    prevHash: DigestBlake2bBlockHeader
    issuerVk: VerificationKey
    issuerVrf: IssuerVrfVerificationKey
    blockSize: BlockSize
    blockHash: DigestBlake2bBlockBody
    opCert: OpCert
    protocolVersion: ProtocolVersion
    signature: IssuerSignature
    vrfInput: CertifiedVrf


class Mary(BaseModel):
    mary: BlockMary


class Point(BaseModel):
    slot: Slot
    hash: DigestBlake2bBlockHeader


class RedeemWitness(BaseModel):
    key: VerificationKey
    signature: Signature


class RollBackward(BaseModel):
    point: PointOrOrigin
    tip: TipOrOrigin


class RollForward(BaseModel):
    block: Block
    tip: TipOrOrigin


class Shelley(BaseModel):
    shelley: BlockShelley


class StandardBlock(BaseModel):
    hash: DigestBlake2bBlockHeader
    header: StandardBlockHeader
    body: StandardBlockBody


class StandardBlockBody(BaseModel):
    txPayload: List[TxByron]
    dlgPayload: List[DlgCertificate]
    updatePayload: UpdatePayload


class StandardBlockHeader(BaseModel):
    blockHeight: BlockNo
    genesisKey: GenesisVerificationKey
    prevHash: DigestBlake2bBlockHeader
    proof: BlockProof
    protocolMagicId: ProtocolMagicId
    protocolVersion: ProtocolVersion
    signature: BlockSignature
    slot: Slot
    softwareVersion: SoftwareVersion


class Tip(BaseModel):
    slot: Slot
    hash: DigestBlake2bBlockHeader
    blockNo: BlockNo


class TxAllegra(BaseModel):
    id: DigestBlake2bBlockBody
    body: TxAllegraBody
    witness: Witness
    metadata: Union[AuxiliaryData, Null]
    raw: str = Field(
        ..., description="The raw serialized transaction, as found on-chain."
    )


class TxAllegraBody(BaseModel):
    inputs: List[TxIn]
    outputs: List[TxOut]
    certificates: List[Certificate]
    withdrawals: Withdrawals
    fee: Lovelace
    validityInterval: ValidityInterval
    update: UpdateShelley


class TxAlonzo(BaseModel):
    id: DigestBlake2bBlockBody
    inputSource: InputSource
    body: TxAlonzoBody
    witness: Witness
    metadata: Union[AuxiliaryData, Null]
    raw: str = Field(
        ..., description="The raw serialized transaction, as found on-chain."
    )


class TxAlonzoBody(BaseModel):
    inputs: List[TxIn]
    collaterals: List[TxIn]
    outputs: List[TxOut]
    certificates: List[Certificate]
    withdrawals: Withdrawals
    fee: Lovelace
    validityInterval: ValidityInterval
    update: UpdateAlonzo
    mint: Value
    network: Union[Network, Null]
    scriptIntegrityHash: Union[DigestBlake2bScriptIntegrity, Null]
    requiredExtraSignatures: List[DigestBlake2bVerificationKey]


class TxBabbage(BaseModel):
    id: DigestBlake2bBlockBody
    inputSource: InputSource
    body: TxBabbageBody
    witness: Witness
    metadata: Union[AuxiliaryData, Null]
    raw: str = Field(
        ..., description="The raw serialized transaction, as found on-chain."
    )


class TxBabbageBody(BaseModel):
    inputs: List[TxIn]
    references: List[TxIn]
    collaterals: List[TxIn]
    collateralReturn: Union[TxOut, Null]
    totalCollateral: Union[Lovelace, Null]
    outputs: List[TxOut]
    certificates: List[Certificate]
    withdrawals: Withdrawals
    fee: Lovelace
    validityInterval: ValidityInterval
    update: UpdateBabbage
    mint: Value
    network: Union[Network, Null]
    scriptIntegrityHash: Union[DigestBlake2bScriptIntegrity, Null]
    requiredExtraSignatures: List[DigestBlake2bVerificationKey]


class TxByron(BaseModel):
    id: TxId
    body: TxByronBody
    witness: List[TxWitness]
    raw: str = Field(
        ..., description="The raw serialized transaction, as found on-chain."
    )


class TxByronBody(BaseModel):
    inputs: List[TxIn]
    outputs: List[TxOut]


class TxIn(BaseModel):
    txId: TxId
    index: UInt32


class TxMary(BaseModel):
    id: DigestBlake2bBlockBody
    body: TxMaryBody
    witness: Witness
    metadata: Union[AuxiliaryData, Null]
    raw: str = Field(
        ..., description="The raw serialized transaction, as found on-chain."
    )


class TxMaryBody(BaseModel):
    inputs: List[TxIn]
    outputs: List[TxOut]
    certificates: List[Certificate]
    withdrawals: Withdrawals
    fee: Lovelace
    validityInterval: ValidityInterval
    update: UpdateShelley
    mint: Value


class TxOut(BaseModel):
    address: Address
    value: Value
    datumHash: Optional[Union[DigestBlake2bDatum, Null]] = None
    datum: Optional[Union[Any, Datum, Null]] = None
    script: Optional[Union[Script, Null]] = None


class TxRedeemWitness(BaseModel):
    redeemWitness: RedeemWitness


class TxShelley(BaseModel):
    id: DigestBlake2bBlockBody
    body: TxShellyBody
    witness: Witness
    metadata: Union[AuxiliaryData, Null]
    raw: str = Field(
        ..., description="The raw serialized transaction, as found on-chain."
    )


class TxShellyBody(BaseModel):
    inputs: List[TxIn]
    outputs: List[TxOut]
    certificates: List[Certificate]
    withdrawals: Withdrawals
    fee: Lovelace
    timeToLive: Slot
    update: UpdateShelley


class TxWitnessVk(BaseModel):
    witnessVk: WitnessVk


class UpdateProposalAlonzo(BaseModel):
    epoch: Epoch
    proposal: Dict[str, ProtocolParametersAlonzo]


class UpdateProposalBabbage(BaseModel):
    epoch: Epoch
    proposal: Dict[str, ProtocolParametersBabbage]


class UpdateProposalShelley(BaseModel):
    epoch: Epoch
    proposal: Dict[str, ProtocolParametersShelley]


class Utxo(BaseModel):
    number: UInt32
    root: DigestBlake2bMerkleRoot
    witnessesHash: WitnessHash


class ValidityInterval(BaseModel):
    invalidBefore: Union[Slot, Null]
    invalidHereafter: Union[Slot, Null]


class WitnessVk(BaseModel):
    key: DigestBlake2bVerificationKey
    signature: Signature


class BootstrapWitness(BaseModel):
    class Config:
        extra = Extra.forbid

    signature: Signature
    chainCode: Union[ChainCode, Null]
    addressAttributes: Union[AddressAttributes, Null]
    key: VerificationKey


class Witness(BaseModel):
    class Config:
        extra = Extra.forbid

    signatures: Dict[str, Signature]
    scripts: Optional[Dict[str, Script]]
    bootstrap: Optional[List[BootstrapWitness]]
    datums: Optional[Dict[str, Datum]]
    redeemers: Optional[Dict[str, Redeemer]]


Block = Babbage | Alonzo | Mary | Allegra | Shelley | Byron

BlockByron = StandardBlock | EpochBoundaryBlock
PointOrOrigin = Union[Point, Origin]

TipOrOrigin = Union[Tip, Origin]

TxWitness = TxWitnessVk | TxRedeemWitness

UpdateAlonzo = Null | UpdateProposalAlonzo

UpdateBabbage = Null | UpdateProposalBabbage

UpdateShelley = Null | UpdateProposalShelley


class SubmitTxErrorMissingVkWitnesses(BaseModel):
    class Config:
        extra = Extra.forbid

    missingVkWitnesses: List[DigestBlake2bVerificationKey]


class SubmitTxErrorMissingScriptWitnesses(BaseModel):
    class Config:
        extra = Extra.forbid

    missingScriptWitnesses: List[DigestBlake2bScript]


class SubmitTxErrorScriptWitnessNotValidating(BaseModel):
    class Config:
        extra = Extra.forbid

    scriptWitnessNotValidating: List[DigestBlake2bScript]


class SubmitTxErrorInsufficientGenesisSignatures(BaseModel):
    class Config:
        extra = Extra.forbid

    insufficientGenesisSignatures: List[DigestBlake2bVerificationKey]


class SubmitTxErrorMissingTxMetadata(BaseModel):
    class Config:
        extra = Extra.forbid

    missingTxMetadata: DigestBlake2bAuxiliaryDataBody


class SubmitTxErrorMissingTxMetadataHash(BaseModel):
    class Config:
        extra = Extra.forbid

    missingTxMetadataHash: DigestBlake2bAuxiliaryDataBody


class TxMetadataHashMismatch(BaseModel):
    class Config:
        extra = Extra.forbid

    includedHash: DigestBlake2bAuxiliaryDataBody
    expectedHash: DigestBlake2bAuxiliaryDataBody


class SubmitTxErrorTxMetadataHashMismatch(BaseModel):
    class Config:
        extra = Extra.forbid

    txMetadataHashMismatch: TxMetadataHashMismatch


class ExpiredUtxo(BaseModel):
    class Config:
        extra = Extra.forbid

    currentSlot: Slot
    transactionTimeToLive: Slot


class SubmitTxErrorExpiredUtxo(BaseModel):
    class Config:
        extra = Extra.forbid

    expiredUtxo: ExpiredUtxo


class TxTooLarge(BaseModel):
    class Config:
        extra = Extra.forbid

    maximumSize: Int64
    actualSize: Int64


class SubmitTxErrorTxTooLarge(BaseModel):
    class Config:
        extra = Extra.forbid

    txTooLarge: TxTooLarge


class SubmitTxErrorMissingAtLeastOneInputUtxo(BaseModel):
    class Config:
        extra = Extra.forbid

    missingAtLeastOneInputUtxo: None


class SubmitTxErrorInvalidMetadata(BaseModel):
    class Config:
        extra = Extra.forbid

    invalidMetadata: None


class FeeTooSmall(BaseModel):
    class Config:
        extra = Extra.forbid

    requiredFee: Lovelace
    actualFee: Lovelace


class SubmitTxErrorFeeTooSmall(BaseModel):
    class Config:
        extra = Extra.forbid

    feeTooSmall: FeeTooSmall


class SubmitTxErrorAddressAttributesTooLarge(BaseModel):
    class Config:
        extra = Extra.forbid

    addressAttributesTooLarge: List[Address]


class SubmitTxErrorTriesToForgeAda(BaseModel):
    class Config:
        extra = Extra.forbid

    triesToForgeAda: None


class SubmitTxErrorDelegateNotRegistered(BaseModel):
    class Config:
        extra = Extra.forbid

    delegateNotRegistered: PoolId


class SubmitTxErrorUnknownOrIncompleteWithdrawals(BaseModel):
    class Config:
        extra = Extra.forbid

    unknownOrIncompleteWithdrawals: Withdrawals


class SubmitTxErrorStakePoolNotRegistered(BaseModel):
    class Config:
        extra = Extra.forbid

    stakePoolNotRegistered: PoolId


class WrongRetirementEpoch(BaseModel):
    class Config:
        extra = Extra.forbid

    currentEpoch: Epoch
    requestedEpoch: Epoch
    firstUnreachableEpoch: Epoch


class SubmitTxErrorWrongRetirementEpoch(BaseModel):
    class Config:
        extra = Extra.forbid

    wrongRetirementEpoch: WrongRetirementEpoch


class UInt8(BaseModel):
    __root__: conint(ge=0, le=255)


class SubmitTxErrorStakeKeyAlreadyRegistered(BaseModel):
    class Config:
        extra = Extra.forbid

    stakeKeyAlreadyRegistered: DigestBlake2bVerificationKey


class PolicyId(BaseModel):
    __root__: DigestBlake2bScript


class PoolCostTooSmall(BaseModel):
    class Config:
        extra = Extra.forbid

    minimumCost: Lovelace


class SubmitTxErrorPoolCostTooSmall(BaseModel):
    class Config:
        extra = Extra.forbid

    poolCostTooSmall: PoolCostTooSmall


class PoolMetadataHashTooBig(BaseModel):
    class Config:
        extra = Extra.forbid

    poolId: PoolId
    measuredSize: Int64


class SubmitTxErrorPoolMetadataHashTooBig(BaseModel):
    class Config:
        extra = Extra.forbid

    poolMetadataHashTooBig: PoolMetadataHashTooBig


class SubmitTxErrorStakeKeyNotRegistered(BaseModel):
    class Config:
        extra = Extra.forbid

    stakeKeyNotRegistered: DigestBlake2bVerificationKey


class SubmitTxErrorRewardAccountNotExisting(BaseModel):
    class Config:
        extra = Extra.forbid

    rewardAccountNotExisting: None


class RewardAccountNotEmpty(BaseModel):
    class Config:
        extra = Extra.forbid

    balance: Lovelace


class SubmitTxErrorRewardAccountNotEmpty(BaseModel):
    class Config:
        extra = Extra.forbid

    rewardAccountNotEmpty: RewardAccountNotEmpty


class SubmitTxErrorWrongCertificateType(BaseModel):
    class Config:
        extra = Extra.forbid

    wrongCertificateType: None


class SubmitTxErrorUnknownGenesisKey(BaseModel):
    class Config:
        extra = Extra.forbid

    unknownGenesisKey: DigestBlake2bVerificationKey


class SubmitTxErrorAlreadyDelegating(BaseModel):
    class Config:
        extra = Extra.forbid

    alreadyDelegating: DigestBlake2bVerificationKey


class InsufficientFundsForMir(BaseModel):
    class Config:
        extra = Extra.forbid

    rewardSource: RewardPot
    sourceSize: Lovelace
    requestedAmount: Lovelace


class SubmitTxErrorInsufficientFundsForMir(BaseModel):
    class Config:
        extra = Extra.forbid

    insufficientFundsForMir: InsufficientFundsForMir


class TooLateForMir(BaseModel):
    class Config:
        extra = Extra.forbid

    currentSlot: Slot
    lastAllowedSlot: Slot


class SubmitTxErrorTooLateForMir(BaseModel):
    class Config:
        extra = Extra.forbid

    tooLateForMir: TooLateForMir


class SubmitTxErrorMirTransferNotCurrentlyAllowed(BaseModel):
    class Config:
        extra = Extra.forbid

    mirTransferNotCurrentlyAllowed: None


class SubmitTxErrorMirNegativeTransferNotCurrentlyAllowed(BaseModel):
    class Config:
        extra = Extra.forbid

    mirNegativeTransferNotCurrentlyAllowed: None


class SubmitTxErrorMirProducesNegativeUpdate(BaseModel):
    class Config:
        extra = Extra.forbid

    mirProducesNegativeUpdate: None


class MirNegativeTransfer(BaseModel):
    class Config:
        extra = Extra.forbid

    rewardSource: RewardPot
    attemptedTransfer: Lovelace


class SubmitTxErrorMirNegativeTransfer(BaseModel):
    class Config:
        extra = Extra.forbid

    mirNegativeTransfer: MirNegativeTransfer


class SubmitTxErrorDuplicateGenesisVrf(BaseModel):
    class Config:
        extra = Extra.forbid

    duplicateGenesisVrf: DigestBlake2bVrfVerificationKey


class NonGenesisVoters(BaseModel):
    class Config:
        extra = Extra.forbid

    currentlyVoting: List[DigestBlake2bVerificationKey]
    shouldBeVoting: List[DigestBlake2bVerificationKey]


class SubmitTxErrorNonGenesisVoters(BaseModel):
    class Config:
        extra = Extra.forbid

    nonGenesisVoters: NonGenesisVoters


class VotingPeriod(Enum):
    voteForThisEpoch = "voteForThisEpoch"
    voteForNextEpoch = "voteForNextEpoch"


class SubmitTxErrorProtocolVersionCannotFollow(BaseModel):
    class Config:
        extra = Extra.forbid

    protocolVersionCannotFollow: ProtocolVersion


class MissingRequiredDatums(BaseModel):
    class Config:
        extra = Extra.forbid

    provided: Optional[List[DigestBlake2bDatum]] = None
    missing: List[DigestBlake2bDatum]


class SubmitTxErrorMissingRequiredDatums(BaseModel):
    class Config:
        extra = Extra.forbid

    missingRequiredDatums: MissingRequiredDatums


class UnspendableDatums(BaseModel):
    class Config:
        extra = Extra.forbid

    nonSpendable: List[DigestBlake2bDatum]
    acceptable: List[DigestBlake2bDatum]


class SubmitTxErrorUnspendableDatums(BaseModel):
    class Config:
        extra = Extra.forbid

    unspendableDatums: UnspendableDatums


class ExtraDataMismatch(BaseModel):
    class Config:
        extra = Extra.forbid

    provided: Union[DigestBlake2bScriptIntegrity, Null]
    inferredFromParameters: Union[DigestBlake2bScriptIntegrity, Null]


class ScriptPurposeSpend(BaseModel):
    class Config:
        extra = Extra.forbid

    spend: TxIn


class ScriptPurposeMint(BaseModel):
    class Config:
        extra = Extra.forbid

    mint: PolicyId


class ScriptPurposeCertificate(BaseModel):
    class Config:
        extra = Extra.forbid

    certificate: Certificate


class ScriptPurposeWithdrawal(BaseModel):
    class Config:
        extra = Extra.forbid

    withdrawal: RewardAccount


class ScriptPurpose(BaseModel):
    __root__: Union[
        ScriptPurposeSpend,
        ScriptPurposeMint,
        ScriptPurposeCertificate,
        ScriptPurposeWithdrawal,
    ]


class NoRedeemer(BaseModel):
    class Config:
        extra = Extra.forbid

    noRedeemer: ScriptPurpose


class NoWitness(BaseModel):
    class Config:
        extra = Extra.forbid

    noWitness: DigestBlake2bScript


class NoCostModel(BaseModel):
    class Config:
        extra = Extra.forbid

    noCostModel: Language


class BadTranslation(BaseModel):
    class Config:
        extra = Extra.forbid

    badTranslation: str = Field(
        ...,
        description="An (hopefully) informative error about the transaction execution failure.",
    )


class SubmitTxErrorCollectErrors(BaseModel):
    class Config:
        extra = Extra.forbid

    collectErrors: List[Union[NoRedeemer, NoWitness, NoCostModel, BadTranslation]]


class SubmitTxErrorExtraDataMismatch(BaseModel):
    class Config:
        extra = Extra.forbid

    extraDataMismatch: ExtraDataMismatch


class SubmitTxErrorMissingRequiredSignatures(BaseModel):
    class Config:
        extra = Extra.forbid

    missingRequiredSignatures: List[DigestBlake2bVerificationKey]


class SubmitTxErrorMissingCollateralInputs(BaseModel):
    class Config:
        extra = Extra.forbid

    missingCollateralInputs: None


class CollateralTooSmall(BaseModel):
    class Config:
        extra = Extra.forbid

    requiredCollateral: Lovelace
    actualCollateral: Lovelace


class SubmitTxErrorCollateralTooSmall(BaseModel):
    class Config:
        extra = Extra.forbid

    collateralTooSmall: CollateralTooSmall


class TooManyCollateralInputs(BaseModel):
    class Config:
        extra = Extra.forbid

    maximumCollateralInputs: UInt64
    actualCollateralInputs: UInt64


class SubmitTxErrorTooManyCollateralInputs(BaseModel):
    class Config:
        extra = Extra.forbid

    tooManyCollateralInputs: TooManyCollateralInputs


class SubmitTxErrorOutsideForecast(BaseModel):
    class Config:
        extra = Extra.forbid

    outsideForecast: Slot


class SubmitTxErrorValidationTagMismatch(BaseModel):
    class Config:
        extra = Extra.forbid

    validationTagMismatch: None


class SubmitTxErrorExtraScriptWitnesses(BaseModel):
    class Config:
        extra = Extra.forbid

    extraScriptWitnesses: List[DigestBlake2bScript]


class ExecutionUnitsTooLarge(BaseModel):
    class Config:
        extra = Extra.forbid

    maximumExecutionUnits: ExUnits
    actualExecutionUnits: ExUnits


class SubmitTxErrorExecutionUnitsTooLarge(BaseModel):
    class Config:
        extra = Extra.forbid

    executionUnitsTooLarge: ExecutionUnitsTooLarge


class SubmitTxErrorUnspendableScriptInputs(BaseModel):
    class Config:
        extra = Extra.forbid

    unspendableScriptInputs: List[TxIn]


class MissingRequiredRedeemers(BaseModel):
    class Config:
        extra = Extra.forbid

    missing: List[Dict[str, ScriptPurpose]]


class UpdateWrongEpoch(BaseModel):
    class Config:
        extra = Extra.forbid

    currentEpoch: Epoch
    requestedEpoch: Epoch
    votingPeriod: VotingPeriod


class SubmitTxErrorWrongPoolCertificate(BaseModel):
    class Config:
        extra = Extra.forbid

    wrongPoolCertificate: UInt8


class SubmitTxErrorUpdateWrongEpoch(BaseModel):
    class Config:
        extra = Extra.forbid

    updateWrongEpoch: UpdateWrongEpoch


class SubmitTxErrorMissingRequiredRedeemers(BaseModel):
    class Config:
        extra = Extra.forbid

    missingRequiredRedeemers: MissingRequiredRedeemers


class InvalidEntityAddress(BaseModel):
    type: InvalidEntityType = InvalidEntityType.ADDRESS
    entity: InvalidEntityEntity = InvalidEntityEntity.ADDRESS


class InvalidEntityPoolRegistration(BaseModel):
    type: InvalidEntityType = InvalidEntityType.POOL_REGISTRATION
    entity: InvalidEntityEntity = InvalidEntityEntity.POOL_REGISTRATION


class InvalidEntityRewardAccount(BaseModel):
    type: InvalidEntityType = InvalidEntityType.REWARD_ACCOUNT
    entity: InvalidEntityEntity = InvalidEntityEntity.REWARD_ACCOUNT


class InvalidEntity(BaseModel):
    __root__: Union[
        InvalidEntityAddress, InvalidEntityPoolRegistration, InvalidEntityRewardAccount
    ]


class NetworkMismatch(BaseModel):
    class Config:
        extra = Extra.forbid

    expectedNetwork: Network
    invalidEntities: List[InvalidEntity]


class SubmitTxErrorNetworkMismatch(BaseModel):
    class Config:
        extra = Extra.forbid

    networkMismatch: NetworkMismatch


class OutputTooSmall(BaseModel):
    class Config:
        extra = Extra.forbid

    output: TxOut
    minimumRequiredValue: Lovelace


class SubmitTxErrorOutputTooSmall(BaseModel):
    class Config:
        extra = Extra.forbid

    outputTooSmall: List[Union[TxOut, OutputTooSmall]]


class SubmitTxErrorTooManyAssetsInOutput(BaseModel):
    class Config:
        extra = Extra.forbid

    tooManyAssetsInOutput: List[TxOut]


class ValueNotConserved(BaseModel):
    class Config:
        extra = Extra.forbid

    consumed: Union[LovelaceDelta, Value]
    produced: Union[LovelaceDelta, Value]


class SubmitTxErrorInvalidWitnesses(BaseModel):
    class Config:
        extra = Extra.forbid

    invalidWitnesses: List[VerificationKey]


class SubmitTxErrorBadInputs(BaseModel):
    class Config:
        extra = Extra.forbid

    badInputs: List[TxIn]


class OutsideOfValidityInterval(BaseModel):
    class Config:
        extra = Extra.forbid

    currentSlot: Slot
    interval: ValidityInterval


class SubmitTxErrorOutsideOfValidityInterval(BaseModel):
    class Config:
        extra = Extra.forbid

    outsideOfValidityInterval: OutsideOfValidityInterval


class SubmitTxErrorValueNotConserved(BaseModel):
    class Config:
        extra = Extra.forbid

    valueNotConserved: ValueNotConserved


class SubmitTxErrorExtraRedeemers(BaseModel):
    class Config:
        extra = Extra.forbid

    extraRedeemers: List[str]


class Era(Enum):
    Byron = "Byron"
    Shelley = "Shelley"
    Allegra = "Allegra"
    Mary = "Mary"
    Alonzo = "Alonzo"
    Babbage = "Babbage"


class EraMismatchObject(BaseModel):
    class Config:
        extra = Extra.forbid

    queryEra: Era
    ledgerEra: Era


class EraMismatch(BaseModel):
    class Config:
        extra = Extra.forbid

    eraMismatch: EraMismatchObject


class SubmitTxErrorCollateralHasNonAdaAssets(BaseModel):
    class Config:
        extra = Extra.forbid

    collateralHasNonAdaAssets: Value


class SubmitTxErrorMissingDatumHashesForInputs(BaseModel):
    class Config:
        extra = Extra.forbid

    missingDatumHashesForInputs: List[TxIn]


class SubmitTxErrorCollateralIsScript(BaseModel):
    class Config:
        extra = Extra.forbid

    collateralIsScript: Utxo


class TotalCollateralMismatch(BaseModel):
    class Config:
        extra = Extra.forbid

    computedFromDelta: Lovelace
    declaredInField: Lovelace


class SubmitTxErrorTotalCollateralMismatch(BaseModel):
    class Config:
        extra = Extra.forbid

    totalCollateralMismatch: TotalCollateralMismatch


class SubmitTxErrorMalformedReferenceScripts(BaseModel):
    class Config:
        extra = Extra.forbid

    malformedReferenceScripts: List[DigestBlake2bScript]


class SubmitTxErrorMalformedScriptWitnesses(BaseModel):
    class Config:
        extra = Extra.forbid

    malformedScriptWitnesses: List[DigestBlake2bScript]


RollForward.update_forward_refs()
BlockBabbage.update_forward_refs()
Witness.update_forward_refs()
TxBabbage.update_forward_refs()
AuxiliaryData.update_forward_refs()
AuxiliaryDataBody.update_forward_refs()
BlockShelley.update_forward_refs()
BlockAllegra.update_forward_refs()
TxOut.update_forward_refs()
BlockMary.update_forward_refs()
BlockAlonzo.update_forward_refs()
SubmitTxErrorCollateralIsScript.update_forward_refs()
