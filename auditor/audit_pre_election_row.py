from dataclasses import dataclass
from typing import Dict, List
from more_itertools import all_equal


from auditor.audit_vote import Commitment
from auditor.audit_table import CommitmentTable
from auditor.audit_tables import TableId, TallyTables


@dataclass
class PreElectionRow:
    left: str
    middle: str
    right: str


PreElectionTable = List[PreElectionRow]
PreElectionTables = Dict[TableId, PreElectionTable]


def audit_pre_election_tables(
    pre_election_tables: PreElectionTables, tally_tables: TallyTables
) -> bool:
    if set(pre_election_tables.keys()) != set(tally_tables.keys()):
        return False

    for key in pre_election_tables:
        if not audit_pre_election_table(pre_election_tables[key], tally_tables[key]):
            return False

    if not all_equal(
        len(pre_election_table) for pre_election_table in pre_election_tables.values()
    ):
        return False

    return True


def audit_pre_election_table(
    pre_election_table: PreElectionTable, commitment_table: CommitmentTable
) -> bool:
    if len(pre_election_table) != len(commitment_table):
        return False

    for pre_election_row, commitment in zip(pre_election_table, commitment_table):
        if not audit_pre_election_row(pre_election_row, commitment):
            return False

    return True


def audit_pre_election_row(
    pre_election_row: PreElectionRow, commitment: Commitment
) -> bool:
    return (
        pre_election_row.left == commitment.left
        and pre_election_row.middle == "0"
        and pre_election_row.right == commitment.right
    )
