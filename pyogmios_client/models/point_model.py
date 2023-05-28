from pyogmios_client.models.Digest_Blake2b_Block_Header import DigestBlake2BBlockHeader
from pyogmios_client.models.base_model import BaseModel

Slot = int
Origin = "origin"
BlockNo = int


class Point(BaseModel):
    slot: Slot
    hash: DigestBlake2BBlockHeader


class Tip(BaseModel):
    slot: Slot
    hash: DigestBlake2BBlockHeader
    block_number: BlockNo


PointOrOrigin = Point | Origin
TipOrOrigin = Tip | Origin
