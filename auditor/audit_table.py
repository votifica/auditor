from typing import List
from more_itertools import all_equal

from auditor.audit_vote import Commitment, OpenedVote, audit_vote


OpenedVoteTable = List[OpenedVote]
CommitmentTable = List[Commitment]


def audit_table(
    opened_votes_table: OpenedVoteTable, commitment_table: CommitmentTable
) -> bool:
    if len(opened_votes_table) == 0:
        print("Opened data empty")
        return False

    if len(opened_votes_table) != len(commitment_table):
        print("Not equal number of rows")
        return False

    # check if all votes has the same side opened
    if not all_equal(bool(opened_vote.left) for opened_vote in opened_votes_table):
        print("Two columns opened")
        return False

    for i, (opened_vote, commitment) in enumerate(zip(opened_votes_table, commitment_table)):
        if audit_vote(opened_vote, commitment) is False:
            print(f"Row {i} commitment is not validating!")
            return False

    return True
