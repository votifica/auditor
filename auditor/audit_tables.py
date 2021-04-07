from typing import Dict

from auditor.audit_table import audit_table, CommitmentTable, OpenedVoteTable


OpenedData = Dict[str, OpenedVoteTable]
CommitmentData = Dict[str, CommitmentTable]


def audit_tables(opened_data: OpenedData, commitment_data: CommitmentData) -> bool:
    # check if opened data has the same keys as commitment data
    if not set(opened_data.keys()) == set(commitment_data.keys()):
        return False

    # check if all corresponding tables are valid
    for key in opened_data:
        if not audit_table(opened_data[key], commitment_data[key]):
            return False

    # check if all tables have the same length
    if len(set([len(opened_table) for opened_table in opened_data.values()])) > 1:
        return False

    return True
