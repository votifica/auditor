from dataclasses import dataclass
from typing import Dict, List

from auditor.audit_table import OpenedVoteTable
from auditor.audit_tables import AuditTables


QuestionId = str
CastCode = str
VoteCode = str
VoteId = str


@dataclass
class BulletinBoardEntry:
    cast_codes: Dict[QuestionId, CastCode]
    vote_codes: Dict[QuestionId, List[VoteCode]]


BulletinBoard = Dict[VoteId, BulletinBoardEntry]


def audit_bb(bb: BulletinBoard, opened_data: AuditTables) -> bool:
    if not any(bool(opened_table[0].left) for opened_table in opened_data.values()):
        print("Opened data has any left column opened")
        return False

    for i, opened_table in enumerate(opened_data.values()):
        if opened_table[0].left:
            if not audit_left_column_bb(bb, opened_table):
                print(f"Invalid left column check for table {i} in opened table")
                return False
        else:
            if not audit_right_column_bb(bb, opened_table):
                print(f"Invalid right column check for table {i} in opened table")
                return False

    return True


def audit_right_column_bb(
    bb: BulletinBoard, opened_vote_table: OpenedVoteTable
) -> bool:
    bb_votes = set()
    num_votes_table = 0

    for i, opened_vote in enumerate(opened_vote_table):
        if opened_vote.right is None:
            print("Table should have right column opened, row {i} doesn't")
            return False

        if opened_vote.middle == 1 or opened_vote.middle == -1:
            num_votes_table += 1

    for bb_entry in bb.values():
        for question_id, cast_code in bb_entry.cast_codes.items():
            for vote_code in bb_entry.vote_codes[question_id]:
                bb_votes.add(f"{question_id}-{cast_code}-{vote_code}")

    if len(bb_votes) == 0:
        print("No votes detected")
        return False

    if not len(bb_votes) == num_votes_table:
        print("Number of votes in the table don't match number of votes on bb")
        return False

    return True


def audit_left_column_bb(bb: BulletinBoard, opened_vote_table: OpenedVoteTable) -> bool:
    bb_votes = set()
    table_votes = set()

    for i, opened_vote in enumerate(opened_vote_table):
        if opened_vote.left is None:
            print("Table should have left column opened, row {i} doesn't")
            return False

        if opened_vote.middle == 1 or opened_vote.middle == -1:
            table_votes.add(opened_vote.left.data)

    for bb_entry in bb.values():
        for question_id, cast_code in bb_entry.cast_codes.items():
            for vote_code in bb_entry.vote_codes[question_id]:
                bb_votes.add(f"{question_id}-{cast_code}-{vote_code}")

    if len(bb_votes) == 0:
        print("No votes detected")
        return False

    if not bb_votes == table_votes:
        print("Number of votes in the table don't match number of votes on bb")
        return False

    return True
