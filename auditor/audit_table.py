from typing import List

from auditor.audit_vote import Commitment, OpenedVote, audit_vote


OpenedVoteTable = List[OpenedVote]
CommitmentTable = List[Commitment]


def audit_table(
    opened_votes_table: OpenedVoteTable, commitment_table: CommitmentTable
) -> bool:
    if len(opened_votes_table) == 0:
        return False

    if len(opened_votes_table) != len(commitment_table):
        return False

    # check if all votes has the same side opened
    if len(set([bool(opened_vote.left) for opened_vote in opened_votes_table])) > 1:
        return False

    for opened_vote, commitment in zip(opened_votes_table, commitment_table):
        if audit_vote(opened_vote, commitment) is False:
            return False

    return True
