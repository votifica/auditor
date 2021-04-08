from pytest import fixture

from auditor.audit_table import OpenedVoteTable
from auditor.audit_tally import audit_right_column_tally, audit_tables_tally, TallyResults
from auditor.audit_tables import AuditTables


@fixture
def tally_results() -> TallyResults:
    return {"0-0": 1, "0-1": 1}


@fixture
def invalid_tally_results() -> TallyResults:
    return {"0-0": 3, "0-1": 2}


def test_audit_tally_results(
    tally_results: TallyResults, right_opened_vote_table: OpenedVoteTable
):
    assert audit_right_column_tally(tally_results, right_opened_vote_table) is True


def test_audit_invalid_tally_results(
    invalid_tally_results: TallyResults, right_opened_vote_table: OpenedVoteTable
):
    assert (
        audit_right_column_tally(invalid_tally_results, right_opened_vote_table)
    ) is False


def test_audit_left_column(
        invalid_tally_results: TallyResults, left_opened_vote_table: OpenedVoteTable
):
    assert (
               audit_right_column_tally(invalid_tally_results, left_opened_vote_table)
           ) is False


def test_audit_opened_data(tally_results: TallyResults, opened_data: AuditTables):
    assert audit_tables_tally(tally_results, opened_data) is True
