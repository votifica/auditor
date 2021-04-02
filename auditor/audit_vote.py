from dataclasses import dataclass
from typing import Optional
import hashlib
import binascii
import hmac


@dataclass
class OpenedLeft:
    key: str
    data: str


@dataclass
class OpenedRight:
    key: str
    data: str


@dataclass
class OpenedVote:
    middle: int
    left: Optional[OpenedLeft] = None
    right: Optional[OpenedRight] = None


@dataclass
class Commitment:
    left: str
    middle: int
    right: str


def audit_vote(opened_vote: OpenedVote, commitment: Commitment):
    if opened_vote.left and opened_vote.right:
        return False

    if opened_vote.left:
        opened_side_vote = opened_vote.left
        commitment_ = commitment.left
    else:
        opened_side_vote = opened_vote.right
        commitment_ = commitment.right

    opened_value_commitment = hmac.new(
        binascii.unhexlify(opened_side_vote.key),
        opened_side_vote.data.encode(),
        hashlib.sha256,
    ).hexdigest()

    return (
        opened_value_commitment == commitment_
        and opened_vote.middle == commitment.middle
    )
