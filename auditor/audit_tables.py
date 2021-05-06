from typing import Dict
from more_itertools import all_equal

from auditor.audit_table import audit_table, CommitmentTable, OpenedVoteTable


TableId = str
AuditTables = Dict[TableId, OpenedVoteTable]
TallyTables = Dict[TableId, CommitmentTable]


def audit_tables(opened_data: AuditTables, commitment_data: TallyTables) -> bool:
    # check if there any tables to audit
    if len(opened_data.keys()) == 0:
        return False

    # check if opened data has the same keys as commitment data
    if set(opened_data.keys()) != set(commitment_data.keys()):
        return False

    # check if all corresponding tables are valid
    for key in opened_data:
        if not audit_table(opened_data[key], commitment_data[key]):
            return False

    # check if all tables have the same length
    if not all_equal(len(opened_table) for opened_table in opened_data.values()):
        return False

    return True
