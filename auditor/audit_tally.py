from typing import Dict

from auditor.audit_table import OpenedVoteTable
from auditor.audit_tables import AuditTables


QuestionAnswerId = str
TallyResults = Dict[QuestionAnswerId, int]


def audit_tables_tally(
    tally_results: TallyResults,
    opened_data: AuditTables,
    count_normal_votes: bool = True,
    count_dummy_votes: bool = True,
) -> bool:
    if not any(bool(opened_table[0].right) for opened_table in opened_data.values()):
        print("At least one table should have right column opened")
        return False

    for key, opened_table in opened_data.items():
        if opened_table[0].right is None:
            continue

        if not audit_right_column_tally(
            tally_results, opened_table, count_normal_votes, count_dummy_votes
        ):
            print(f"Tally validation fails for table {key} from opened_data")
            return False

    return True


def audit_right_column_tally(
    tally_results: TallyResults,
    opened_vote_table: OpenedVoteTable,
    count_normal_votes: bool = True,
    count_dummy_votes: bool = True,
) -> bool:
    results = {}

    for i, opened_vote in enumerate(opened_vote_table):
        if opened_vote.right is None:
            print(f"Row {i} doesn't have right column opened")
            return False

        if (count_normal_votes and opened_vote.middle == 1) or (
            count_dummy_votes and opened_vote.middle == -1
        ):
            if (question_answer_id := opened_vote.right.data) not in results:
                results[question_answer_id] = 1
            else:
                results[question_answer_id] += 1

    if results != tally_results:
        print(f"Tally results {tally_results} does not match table results {results}")
        return False

    return True
