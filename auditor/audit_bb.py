from dataclasses import dataclass
from typing import Dict, List

from auditor.audit_table import OpenedVoteTable


@dataclass
class BulletinBoardEntry:
    cast_codes: Dict[str, str]
    vote_codes: Dict[str, List[str]]


BulletinBoard = Dict[str, BulletinBoardEntry]


def audit_bb_table(bb: BulletinBoard, opened_vote_table: OpenedVoteTable) -> bool:
    return True



