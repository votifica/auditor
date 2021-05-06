from typing import Dict

from auditor.audit_table import OpenedVoteTable
from auditor.audit_tables import AuditTables


QuestionAnswerId = str
TallyResults = Dict[QuestionAnswerId, int]


def audit_tables_tally(tally_results: TallyResults, opened_data: AuditTables) -> bool:
    if not any(bool(opened_table[0].right) for opened_table in opened_data.values()):
        return False

    for opened_table in opened_data.values():
        if opened_table[0].right is None:
            continue

        if not audit_right_column_tally(tally_results, opened_table):
            return False

    return True


def audit_right_column_tally(
    tally_results: TallyResults, opened_vote_table: OpenedVoteTable
) -> bool:
    results = {}

    for opened_vote in opened_vote_table:
        if opened_vote.right is None:
            return False

        if opened_vote.middle == 1:
            if (question_answer_id := opened_vote.right.data) not in results:
                results[question_answer_id] = 1
            else:
                results[question_answer_id] += 1

    return results == tally_results
